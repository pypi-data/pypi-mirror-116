#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#
"""Data-types representing Anaml aggregations."""

from abc import ABC, abstractmethod

from jsonschema import validate

from .schema import (
    aggregate_schema,
)


class Aggregation(ABC):
    def __init__(self):
        pass

    def __str__(self):
        return "DataType()"

    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    def from_json(cls, d):
        validate(d, aggregate_schema)
        return cls.from_dict(d)

    @classmethod
    def from_dict(cls, d):
        if d is None:
            return None
        elif d["adt_type"] == "sum":
            return SumAggregation()
        elif d["adt_type"] == "count":
            return CountAggregation()
        elif d["adt_type"] == "countdistinct":
            return CountDistinctAggregation()
        elif d["adt_type"] == "avg":
            return AverageAggregation()
        elif d["adt_type"] == "std":
            return StdAggregation()
        elif d["adt_type"] == "last":
            return LastAggregation()
        elif d["adt_type"] == "percentagechange":
            return PercentageChangeAggregation()
        elif d["adt_type"] == "absolutechange":
            return AbsoluteChangeAggregation()
        elif d["adt_type"] == "standardscore":
            return StandardScoreAggregation()
        else:
            raise ValueError("Bad window specification")


class SumAggregation(Aggregation):
    """Represents a `sum` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new SumAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, SumAggregation)

    def __str__(self):
        return "SumAggregation()"

    def to_dict(self):
        return {"adt_type": "sum"}


class CountAggregation(Aggregation):
    """Represents a `count` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new CountAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, CountAggregation)

    def __str__(self):
        return "CountAggregation()"

    def to_dict(self):
        return {"adt_type": "count"}


class CountDistinctAggregation(Aggregation):
    """Represents a `count_distinct` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new CountDistinctAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, CountDistinctAggregation)

    def __str__(self):
        return "CountDistinctAggregation()"

    def to_dict(self):
        return {"adt_type": "countdistinct"}


class AverageAggregation(Aggregation):
    """Represents an `average` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new AverageAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, AverageAggregation)

    def __str__(self):
        return "AverageAggregation()"

    def to_dict(self):
        return {"adt_type": "avg"}


class StdAggregation(Aggregation):
    """Represents a `std` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new StdAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, StdAggregation)

    def __str__(self):
        return "StdAggregation()"

    def to_dict(self):
        return {"adt_type": "std"}


class LastAggregation(Aggregation):
    """Represents a `last` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new LastAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, LastAggregation)

    def __str__(self):
        return "LastAggregation()"

    def to_dict(self):
        return {"adt_type": "last"}


class PercentageChangeAggregation(Aggregation):
    """Represents a `percentage_change` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new PercentageChangeAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, PercentageChangeAggregation)

    def __str__(self):
        return "PercentageChangeAggregation()"

    def to_dict(self):
        return {"adt_type": "percentagechange"}


class AbsoluteChangeAggregation(Aggregation):
    """Represents an `absolute_change` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new AbsoluteChangeAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, AbsoluteChangeAggregation)

    def __str__(self):
        return "AbsoluteChangeAggregation()"

    def to_dict(self):
        return {"adt_type": "absolutechange"}


class StandardScoreAggregation(Aggregation):
    """Represents a `standard_score` aggregation for a `feature.aggregate`"""

    def __init__(self):
        """Creates a new StandardScoreAggregation"""
        super().__init__()

    def __eq__(self, other):
        return isinstance(other, StandardScoreAggregation)

    def __str__(self):
        return "StandardScoreAggregation()"

    def to_dict(self):
        return {"adt_type": "standardscore"}
