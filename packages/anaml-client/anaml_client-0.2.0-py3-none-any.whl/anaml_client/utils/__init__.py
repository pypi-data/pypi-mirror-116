#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#
"""Utility functions, mostly for internal use."""

import builtins
import dataclasses
import sys

from datetime import datetime, timezone
from typing import Optional

INSTANT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def parse_bool(t: str) -> bool:
    """Parse case insensitive "true" and "false" strings to bool."""
    if isinstance(t, bool):
        return t
    elif isinstance(t, str):
        s = t.lower()
        if s == "true":
            return True
        elif s == "false":
            return False
    else:
        raise ValueError(f"Invalid boolean value: {t}")


def parse_instant(t: str) -> datetime:
    """Parse a Scala Instant to a datetime."""
    dt_from_str = datetime.strptime(t, INSTANT_FORMAT)
    dt_from_str = dt_from_str.replace(tzinfo=timezone.utc)
    return dt_from_str


def parse_instant_optional(t: Optional[str]) -> Optional[datetime]:
    """Parse an optional Scala Instant to an optional datetime."""
    if t is None:
        return None
    return parse_instant(t)


def map_opt(o, f):
    """If a value is non-None, apply the function to it."""
    return f(o) if o is not None else None


# We use this so we can distinguish between the an optional argument that was not given, and
# one that was given with the value None.
class _MissingType:
    def __repr__(self):
        return 'None'


_MISSING = _MissingType()
_COPY_METHOD_NAME = "copy"
_PERSISTENT_METHOD_MARKER = "__persistent_method__"


def _create_fn(name, args, body, *, doc=None, globals=None, locals=None, return_type=_MISSING):
    # This is stolen from dataclasses with the addition of doc.

    # Note that we mutate locals when exec() is called.  Caller
    # beware!  The only callers are internal to this module, so no
    # worries about external callers.
    if locals is None:
        locals = {}
    if 'BUILTINS' not in locals:
        locals['BUILTINS'] = builtins
    return_annotation = ''
    if return_type is not _MISSING:
        locals['_return_type'] = return_type
        return_annotation = '->_return_type'
    args = ','.join(args)
    body = '\n'.join(f'  {b}' for b in body)

    # Compute the text of the entire function.
    txt = f' def {name}({args}){return_annotation}:\n{body}'

    local_vars = ', '.join(locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"

    ns = {}
    exec(txt, globals, ns)
    f = ns['__create_fn__'](**locals)

    # We use this to mark all methods we generate. This lets us replace them when processing subclasses without
    # accidentally also replacing methods defined by the client.
    setattr(f, _PERSISTENT_METHOD_MARKER, True)

    if doc is not None:
        f.__doc__ = doc

    return f


def _copy_param(f):
    """Construct the Python source string to declare a parameter for the copy function."""
    # We can only handle fields with init=True.
    return f'{f.name}: Optional[_type_{f.name}] = MISSING' if f.init else ''


def _make_copy_fn(cls, method_name: str, self_name: str, globals):
    # Build a copy() method. This method accepts keyword parameters for every dataclass field declared with
    # field.init. It creates and returns a new instance with the existing values together with each of the
    # keyword arguments actually given.
    locals = {
        'MISSING': _MISSING,
        'Optional': Optional,
        '__my_klass__': cls,
    }
    parameters = [self_name]
    body_lines = ['values = {}']

    fields = dataclasses.fields(cls)

    for f in fields:
        if f.init:
            # Add the field type to the locals so that it's available when the parameter definition is evaluated.
            locals[f'_type_{f.name}'] = f.type
            # Add the parameter definition to the function code.
            parameters.append(_copy_param(f))
            # Add code to copy or override the fields.
            body_lines += [
                f'if {f.name} is MISSING:',
                f'  values["{f.name}"] = getattr(self, "{f.name}")',
                'else:',
                f'  values["{f.name}"] = {f.name}',
            ]

    # Finally, return a new instance with the values we copied.
    body_lines.append(
        'return __my_klass__(**values)'
    )

    doc = "Return a copy of this object with the specified fields overridden."

    return _create_fn(
        method_name,
        parameters,
        body_lines,
        doc=doc,
        locals=locals,
        globals=globals,
        return_type=cls,
    )


def _process_persistent(cls):
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"{cls.__name__} is not a dataclass; only data classes can be made persistent")

    # We don't want to silently obliterate methods defined by the user, but we also don't
    # want to assume that they added the decorator for no reason whatsoever.
    if hasattr(cls, _COPY_METHOD_NAME) and not hasattr(getattr(cls, _COPY_METHOD_NAME), _PERSISTENT_METHOD_MARKER):
        raise TypeError(
            f"Cannot make {cls.__name__} persistent: it already has a method or field called '{_COPY_METHOD_NAME}'"
        )

    class_globals = sys.modules[cls.__module__].__dict__
    self_name = "__self__" if "self" in dataclasses.fields(cls) else "self"

    setattr(cls, _COPY_METHOD_NAME, _make_copy_fn(cls, _COPY_METHOD_NAME, self_name, class_globals))

    return cls


def persistent(cls=None):
    """Enhance frozen dataclasses with helper methods."""

    def wrap(cls):
        return _process_persistent(cls)

    if cls is None:
        return wrap

    return wrap(cls)
