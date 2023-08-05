#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#
"""Data-types for Anaml window expressions."""

from jsonschema import validate

from .schema import window_schema
from abc import ABC, abstractmethod


class Window(ABC):
    def __init__(self):
        pass

    def __repr__(self):
        return "Window()"

    def __str__(self):
        return "Window()"

    @abstractmethod
    def to_json(self):
        pass

    @classmethod
    def from_json(cls, d):
        validate(d, window_schema)
        cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        if d["adt_type"] == "rowwindow":
            return RowWindow(d["rows"])
        elif d["adt_type"] == "daywindow":
            return DayWindow(d["days"])
        elif d["adt_type"] == "openwindow":
            return OpenWindow()
        else:
            raise ValueError("Bad window specification")


class OpenWindow(Window):
    def __init__(self):
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, OpenWindow)

    def __repr__(self):
        return "OpenWindow()"

    def to_json(self):
        return {"adt_type": "openwindow"}


class RowWindow(Window):
    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def __eq__(self, other):
        if not isinstance(other, RowWindow):
            return NotImplemented
        return self.rows == other.rows

    def __repr__(self):
        return "RowWindow(rows={rows})".format(rows=self.rows)

    def to_json(self):
        return {"adt_type": "rowwindow", "rows": self.rows}


class DayWindow(Window):
    def __init__(self, days):
        super().__init__()
        self.days = days

    def __eq__(self, other):
        if not isinstance(other, DayWindow):
            return NotImplemented
        return self.days == other.days

    def __repr__(self):
        return "DayWindow(days={days})".format(days=self.days)

    def to_json(self):
        return {"adt_type": "daywindow", "days": self.days}
