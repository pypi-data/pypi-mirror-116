#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#

"""Data types for Anaml Check definitions."""

from __future__ import annotations

from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional, Type
import enum
from uuid import UUID

from .schema import check_schema, check_status_field, check_conclusion_field, check_components_schema
from ..model import AnamlBaseClass, INSTANT_FORMAT, json_safe
from ..utils import map_opt, parse_instant_optional


@enum.unique
class CheckStatus(enum.Enum):
    Pending = 'pending'
    Running = 'running'
    Completed = 'completed'

    @classmethod
    def json_schema(cls) -> dict:
        return check_status_field

    # @classmethod
    # def from_dict(cls: Type[CheckStatus], data: dict) -> CheckStatus:
    #     return cls(data['adt_type'])

    def to_json(self) -> str:
        return self.value


class CheckConclusion(enum.Enum):
    Cancelled = 'cancelled'
    Failure = 'failure'
    Success = 'success'
    Skipped = 'skipped'
    TimedOut = 'timedout'

    @classmethod
    def json_schema(cls) -> dict:
        return check_conclusion_field

    # @classmethod
    # def from_dict(cls: Type[CheckConclusion], data: dict) -> CheckConclusion:
    #     return cls(data['adt_type'])

    def to_json(self) -> str:
        return self.value


@dataclass(frozen=True)
class CheckComponent(AnamlBaseClass):
    """Result of a check against an individual component in the catalog"""
    key: str
    value: str

    @classmethod
    def json_schema(cls) -> dict:
        return check_components_schema

    def to_json(self) -> dict:
        return json_safe(self.to_dict())

    @classmethod
    def from_dict(cls: Type[CheckComponent], data: dict) -> Check:
        return CheckComponent(
            key=data['key'],
            value=data['value']
        )


@dataclass(frozen=True)
class Check(AnamlBaseClass):
    """Result of running checks against the Anaml catalogue"""
    name: str
    commit: UUID
    status: CheckStatus
    components: list[CheckComponent] = field(default_factory=list)
    created_by: Optional[int] = None
    id: Optional[int] = None
    started: Optional[datetime] = datetime.now().astimezone(timezone.utc)
    completed: Optional[datetime] = None
    conclusion: Optional[CheckStatus] = None
    details_url: Optional[str] = None

    def with_status(self, new_status: CheckStatus) -> Check:
        dict = self.to_dict()
        dict['status'] = new_status
        if (new_status == CheckStatus.Completed):
            dict['completed'] = datetime.now().astimezone(timezone.utc)
        return Check(**dict)

    def with_conclusion(self, new_conclusion: CheckConclusion) -> Check:
        dict = self.to_dict()
        dict['conclusion'] = new_conclusion
        return Check(**dict)

    def with_component(self, new_component: CheckComponent) -> Check:
        dict = self.to_dict()
        dict['components'].append(new_component.to_json())
        return Check(**dict)

    @classmethod
    def json_schema(cls) -> dict:
        return check_schema

    def to_json(self) -> dict:
        return json_safe(
            self.to_dict(),
            datetime_format=INSTANT_FORMAT
        )

    @classmethod
    def from_dict(cls: Type[Check], data: dict) -> Check:
        return Check(
            id=data['id'],
            name=data['name'],
            commit=UUID(hex=data['commit']),
            created_by=data['created_by'],
            started=parse_instant_optional(data['started']),
            completed=parse_instant_optional(data['completed']),
            status=CheckStatus(data['status']),
            components=[CheckComponent.from_dict(c) for c in data['components']],
            conclusion=map_opt(data['conclusion'], lambda x: CheckConclusion(x)),
            details_url=data['details_url']
        )
