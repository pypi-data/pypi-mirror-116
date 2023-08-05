#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#
"""Data types for Anaml statistics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar, Type

from .schema import (
    feature_statistics,
    numerical_feature_statistics,
    categorical_feature_statistics,
    empty_feature_statistics,
    default_feature_statistics,
    category_frequency
)
from ..model import AnamlBaseClass


@dataclass(frozen=True)
class SummaryStatistics(AnamlBaseClass):
    """Abstract class representing Anaml summary statistics."""

    ADT_TYPE: ClassVar[str] = ""
    adt_type: str = field(default=ADT_TYPE, init=False, repr=False)

    featureName: str

    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for summary statistics objects."""
        return feature_statistics

    @classmethod
    def from_dict(cls: Type[SummaryStatistics], data: dict) -> SummaryStatistics:
        """Parse a summary statistics object from valid JSON data."""
        adt_type = data.get('adt_type', None)
        for klass in cls.__subclasses__():
            if adt_type == klass.ADT_TYPE:
                return klass.from_dict(data)
        raise ValueError(f"Cannot parse JSON for cluster: Unknown adt_type '{adt_type}'")


@dataclass(frozen=True)
class NumericalSummaryStatistics(SummaryStatistics):
    """Summary stats for a numerical column."""

    ADT_TYPE: ClassVar[str] = "numerical"
    adt_type: str = field(default=ADT_TYPE, init=False, repr=False)

    count: int
    min: float
    max: float
    stdDev: float
    mean: float
    quantiles: list[float]

    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for numerical summary statistics objects."""
        return numerical_feature_statistics

    @classmethod
    def from_dict(cls: Type[NumericalSummaryStatistics], data: dict) -> NumericalSummaryStatistics:
        """Parse a numerical summary statistics object from valid JSON data."""
        return NumericalSummaryStatistics(
            featureName=data['featureName'],
            count=data['count'],
            min=data['min'],
            max=data['max'],
            mean=data['mean'],
            stdDev=data['stdDev'],
            quantiles=data['quantiles'],
        )


@dataclass(frozen=True)
class CategoryFrequency(AnamlBaseClass):
    """Metadata attributes."""

    category: str
    frequency: int

    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for category frequency objects."""
        return category_frequency

    @classmethod
    def from_dict(cls: Type[CategoryFrequency], data: dict) -> CategoryFrequency:
        """Parse a category frequency object from valid JSON data."""
        return CategoryFrequency(
            category=data['category'],
            frequency=data['frequency']
        )


@dataclass(frozen=True)
class CategoricalSummaryStatistics(SummaryStatistics):
    """Summary stats for a numerical column."""

    ADT_TYPE: ClassVar[str] = "categorical"
    adt_type: str = field(default=ADT_TYPE, init=False, repr=False)

    count: int
    categoryFrequencies: list[CategoryFrequency]

    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for categorical summary statistics objects."""
        return categorical_feature_statistics

    @classmethod
    def from_dict(cls: Type[CategoricalSummaryStatistics], data: dict) -> CategoricalSummaryStatistics:
        """Parse a categorical summary statistics object from valid JSON data."""
        return CategoricalSummaryStatistics(
            featureName=data['featureName'],
            count=data['count'],
            categoryFrequencies=[
                    CategoryFrequency(category=i['category'], frequency=i['frequency'])
                    for i in data['categoryFrequencies']
                ],
        )


@dataclass(frozen=True)
class DefaultSummaryStatistics(SummaryStatistics):
    """Summary stats for a numerical column."""

    ADT_TYPE: ClassVar[str] = "default"
    adt_type: str = field(default=ADT_TYPE, init=False, repr=False)

    count: int

    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for default summary statistics objects."""
        return default_feature_statistics

    @classmethod
    def from_dict(cls: Type[DefaultSummaryStatistics], data: dict) -> DefaultSummaryStatistics:
        """Parse a default summary statistics object from valid JSON data."""
        return DefaultSummaryStatistics(
            featureName=data['featureName'],
            count=data['count'],
        )


@dataclass(frozen=True)
class EmptySummaryStatistics(SummaryStatistics):
    """Summary stats for a numerical column."""

    ADT_TYPE: ClassVar[str] = "empty"
    adt_type: str = field(default=ADT_TYPE, init=False, repr=False)

    @classmethod
    def json_schema(cls) -> dict:
        """JSON schema for empty summary statistics objects."""
        return empty_feature_statistics

    @classmethod
    def from_dict(cls: Type[EmptySummaryStatistics], data: dict) -> EmptySummaryStatistics:
        """Parse an empty statistics object from valid JSON data."""
        return EmptySummaryStatistics(
            featureName=data['featureName'],
        )
