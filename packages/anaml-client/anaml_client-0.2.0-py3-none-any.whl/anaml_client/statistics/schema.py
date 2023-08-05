#
# Copyright 2021 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium is
# strictly prohibited.
#
"""JSON Schemas definitions for statistics."""

from ..model.schema import json_list

numerical_feature_statistics = {
    "type": "object",
    "properties": {
        "adt_type": {
            "type": "string",
            "enum": ["numerical"],
        },
        "featureName": {"type": "string"},
        "count": {"type": "integer"},
        "min": {"type": "number"},
        "max": {"type": "number"},
        "mean": {"type": "number"},
        "stdDev": {"type": "number"},
        "quantiles": json_list({"type": "number"}),
    },
    "required": ["adt_type", "featureName", "count", "min", "max", "mean", "stdDev", "quantiles"]
}


category_frequency = {
    "type": "object",
    "properties": {
        "category": {"type": "string"},
        "frequency": {"type": "integer"},
    },
    "required": ["category", "frequency"]
}

categorical_feature_statistics = {
    "type": "object",
    "properties": {
        "adt_type": {
            "type": "string",
            "enum": ["categorical"],
        },
        "featureName": {"type": "string"},
        "count": {"type": "integer"},
        "categoryFrequencies": json_list(category_frequency)
    },
    "required": ["adt_type", "featureName", "count", "categoryFrequencies"]
}

default_feature_statistics = {
    "type": "object",
    "properties": {
        "adt_type": {
            "type": "string",
            "enum": ["default"],
        },
        "featureName": {"type": "string"},
        "count": {"type": "integer"},
    },
    "required": ["adt_type", "featureName", "count"]
}

empty_feature_statistics = {
    "type": "object",
    "properties": {
        "adt_type": {
            "type": "string",
            "enum": ["empty"],
        },
        "featureName": {"type": "string"},
    },
    "required": ["adt_type", "featureName"]
}


feature_statistics = {
    "allOf": [
        {
            "type": "object",
            "required": ["adt_type", "featureName"],
            "properties": {
                "adt_type": {
                    "type": "string",
                    "enum": ["numerical", "categorical", "default", "empty"]
                },
                "featureName": {"type": "string"},
            },
        },
        {
            "oneOf": [
                numerical_feature_statistics,
                categorical_feature_statistics,
                default_feature_statistics,
                empty_feature_statistics
            ]
        }
    ]
}
