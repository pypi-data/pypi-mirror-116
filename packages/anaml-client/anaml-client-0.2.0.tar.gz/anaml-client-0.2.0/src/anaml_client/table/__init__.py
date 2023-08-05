#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#
"""Data types for Anaml table definitions."""

from __future__ import annotations

import uuid

from dataclasses import dataclass
from typing import Optional

from ..model import (
    AnamlBaseClass, Attribute, EntityId, EntityMappingId, FeatureId, Label, QualityRating, SourceReference
)


#
# These data type declarations must be kept in sync with
# {repo_top}/common/src/main/scala/io/anaml/common/model
#
# Abbreviations for location clues:
#
# REPO = anaml-server/
# COMMON = anaml-server/common
# MODEL = anaml-server/common/src/main/scala/io/anaml/common/model
# PYCLIENT = anaml-server/python-client/src


#
# TableData $MODEL/TableData.scala
#
TableName = str
TableVersionId = uuid.UUID
TableId = int


class InvalidTableException(Exception):
    """Exception raised when an invalid table specification is give."""


class UnknownTableTypeException(Exception):
    """Exception raised when an unknown table type is given."""


# This matches up to the _name_ of the column extracted from a DB, which
# is why it's text rather than a timestamp object
@dataclass(frozen=True)
class TimestampInfo(AnamlBaseClass):
    """Configuration for the source of timestamp information in a table."""

    timestampColumn: str
    timezone: Optional[str]

    @classmethod
    def json_schema(cls) -> Optional[dict]:
        """JSON schema for timestamp information objects."""
        # TODO: JSON schema for timestamp info.
        return None

    @classmethod
    def from_dict(cls, d: dict) -> TimestampInfo:
        """Parse a timestamp info object from valid JSON data."""
        return TimestampInfo(
            timestampColumn=d["timestampColumn"],
            timezone=d.get("timezone", None)
        )


@dataclass(frozen=True)
class EventDescription(AnamlBaseClass):
    """Event description information for table a definition."""

    entities: dict[EntityId, str]
    timestampInfo: TimestampInfo

    @classmethod
    def json_schema(cls) -> Optional[dict]:
        """JSON schema for event description objects."""
        # TODO: JSON schema for event description.
        return None

    @classmethod
    def from_dict(cls, d: dict):
        """Parse an event description from valid JSON data."""
        return EventDescription(
            entities={int(k): str(v) for k, v in d["entities"].items()},
            timestampInfo=TimestampInfo.from_dict(d["timestampInfo"])
        )


@dataclass(frozen=True)
class Table(AnamlBaseClass):
    """Base class for table definitions."""

    id: int
    name: TableName
    description: Optional[str]
    qualityRating: Optional[QualityRating]
    version: TableVersionId
    labels: list[Label]
    attributes: list[Attribute]

    @classmethod
    def json_schema(cls) -> Optional[dict]:
        """JSON schema for table objects."""
        # TODO: Implement JSON schema for table.
        return None

    @classmethod
    def from_dict(cls, d: dict):
        """Parse a table from valid JSON data."""
        # TODO: Refactor to use the new pattern for class-clusters.
        adt = d.get("adt_type", None)
        if not adt:
            raise InvalidTableException("Table adt_type unspecified")
        # Should be a switch+case
        elif adt == "root":
            return RootTable.from_dict(d)
        elif adt == "pivot":
            return PivotTable.from_dict(d)
        elif adt == "view":
            return ViewTable.from_dict(d)
        else:
            raise UnknownTableTypeException(f"Table adt_type {adt} unknown")

    @classmethod
    def _base_fields(cls, data: dict) -> dict:
        """Parse common table fields from valid JSON data."""
        quality_rating = data.get("qualityRating", None)
        if quality_rating:
            quality_rating = QualityRating(quality_rating)
        return dict(
            id=int(data["id"]),
            name=data["name"],
            description=data.get("description", None),
            qualityRating=quality_rating,
            version=uuid.UUID(hex=data["version"]),
            labels=data["labels"],
            attributes=[Attribute.from_dict(a) for a in data["attributes"]]
        )


@dataclass(frozen=True)
class RootTable(Table):
    """Definition of a root table."""

    source: SourceReference
    eventDescription: Optional[EventDescription]

    @classmethod
    def json_schema(cls) -> Optional[dict]:
        """JSON schema for root table objects."""
        # TODO: JSON schema for root table.
        return None

    @classmethod
    def from_dict(cls, data: dict):
        """Parse a root table from valid JSON data."""
        # TODO: Refactor to follow new pattern for handling optional fields.
        event_description = data.get('eventDescription', None)
        if event_description:
            event_description = EventDescription.from_dict(event_description)
        return RootTable(
            **Table._base_fields(data),
            source=SourceReference.from_dict(data["source"]),
            eventDescription=event_description
        )


@dataclass(frozen=True)
class ViewTable(Table):
    """Definition of a view table."""

    eventDescription: Optional[EventDescription]
    expression: str
    sources: list[TableId]

    @classmethod
    def json_schema(cls) -> Optional[dict]:
        """JSON schema for view table objects."""
        # TODO: JSON schema for view table.
        return None

    @classmethod
    def from_dict(cls, data: dict):
        """Parse a view table from valid JSON data."""
        # TODO: Refactor to use new pattern for handling optional fields.
        event_description = data.get('eventDescription', None)
        if event_description:
            event_description = EventDescription.from_dict(event_description)

        return ViewTable(
            **Table._base_fields(data),
            eventDescription=event_description,
            expression=data["expression"],
            sources=[int(s) for s in data["sources"]],
        )


@dataclass(frozen=True)
class PivotTable(Table):
    """Definition for pivot tables."""

    entityMapping: EntityMappingId
    extraFeatures: list[FeatureId]

    @classmethod
    def json_schema(cls) -> Optional[dict]:
        """JSON schema for pivot table objects."""
        # TODO: JSON schema for pivot table.
        return None

    @classmethod
    def from_dict(cls, data: dict):
        """Parse a pivot table from valid JSON data."""
        return PivotTable(
            **Table._base_fields(data),
            entityMapping=int(data["entityMapping"]),
            extraFeatures=[int(f) for f in data["extraFeatures"]]
        )
