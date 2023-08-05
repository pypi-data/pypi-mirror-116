#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#
"""Data-types for Anaml SQL expressions."""

from jsonschema import validate

from .schema import (
    select_schema,
)


class SelectExpression(object):
    """SQL Expression for the Feature Aggregation"""

    def __init__(self, sql: str):
        """
        Initialise the object

        Arguments:
            sql: String SQL Expression
        """
        self.sql = sql

    def __eq__(self, other):
        if not isinstance(other, SelectExpression):
            return NotImplemented
        return self.sql == other.sql

    def __repr__(self):
        return "SelectExpression(sql={sql})".format(sql=self.sql)

    @classmethod
    def from_dict(cls, d):
        return SelectExpression(d["sql"])

    def to_dict(self):
        return {"sql": self.sql}


class FilterExpression(object):
    """SQL Expression for the feature data filtering"""

    def __init__(self, sql: str):
        """
        Initialise the object

        Arguments:
            sql: String SQL `where` clause
        """
        self.sql = sql

    def __eq__(self, other):
        if not isinstance(other, FilterExpression):
            return NotImplemented
        return self.sql == other.sql

    def __repr__(self):
        return "FilterExpression(sql={sql})".format(sql=self.sql)

    @classmethod
    def from_json(cls, d):
        validate(d, select_schema)
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        if d is None:
            return None
        else:
            return FilterExpression(d["sql"])

    def to_dict(self):
        return {"sql": self.sql}


class PostAggregateExpression(object):
    def __init__(self, sql):
        self.sql = sql

    def __eq__(self, other):
        if not isinstance(other, PostAggregateExpression):
            return NotImplemented
        return self.sql == other.sql

    def __repr__(self):
        return "PostAggregateExpression(sql={sql})".format(sql=self.sql)

    @classmethod
    def from_dict(cls, d):
        if d is None:
            return None
        else:
            return PostAggregateExpression(d["sql"])

    def to_dict(self):
        return {"sql": self.sql}
