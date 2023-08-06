#
# Copyright 2020 Simple Machines Pty Ltd - All Rights Reserved.
#
# This file is part of Anaml.
#
# Unauthorized copying and/or distribution of this file, via any medium
# is strictly prohibited.
#
"""JSON Schema definitions for feature definitions and related objects."""


data_type_schema = {
    "type": "object",
    "properties": {
        "adt_type": {
            "type": "string",
            "enum": ["int", "string", "bigint", "double", "float",
                     "date", "timestamp"]
        }
    },
    "required": ["adt_type"]
}

aggregate_schema = {
    "type": "object",
    "properties": {
        "adt_type": {
            "type": "string",
            "enum": ["sum", "count", "countdistinct", "avg", "std",
                     "last", "percentagechange", "absolutechange",
                     "standardscore"]
        }
    },
    "required": ["adt_type"]
}

post_aggregate_schema = {
    "type": "object",
    "properties": {
        "sql": {"type": "string"}
    },
    "required": ["sql"]
}

# {'days': 14, 'adt_type': 'daywindow'}
window_schema = {
    "type": "object",
    "properties": {
        "adt_type": {"type": "string",
                     "enum": ["openwindow", "daywindow", "rowwindow"]}
    },
    "required": ["adt_type"],
    "allOf": [
        {
            "if": {"properties": {"adt_type": {"const": "daywindow"}}},
            "then": {"properties": {"days": {"type": "integer"}}}
        },
        {
            "if": {"properties": {"adt_type": {"const": "rowwindow"}}},
            "then": {"properties": {"rows": {"type": "integer"}}}
        }
    ]
}

select_schema = {
    "type": "object",
    "properties": {"sql": {"type": "string"}}
}

filter_schema = {
    "type": ["null", "object"],
    "properties": {"sql": {"type": "string"}}
}

feature_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "adt_type": {"type": "string", "enum": ["event", "row"]}
    },
    "required": ["name", "adt_type"],
    "allOf": [
        {
            "if": {"properties": {"adt_type": {"const": "event"}}},
            "then": {
                "properties": {
                    "table": {"type": "integer"},
                    "window": window_schema,
                    "select": select_schema,
                    "filter": filter_schema,
                    "aggregate": aggregate_schema,
                    "postAggregateExpr": {"anyOf": [{"type": "null"},
                                          post_aggregate_schema]}
                },
                "required": ["table", "window", "select", "aggregate"]
            }
        },
        {
            "if": {"properties": {"adt_type": {"const": "row"}}},
            "then": {
                "properties": {
                    "entityId": {"type": "integer"},
                    "select": select_schema,
                    "over": {"type": "array", "items": {"type": "integer"}}
                },
                "required": ["over", "select", "entityId"]
            }
        }
    ]
}

feature_template_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "adt_type": {"type": "string", "enum": ["event"]}
    },
    "required": ["name", "adt_type"],
    "allOf": [
        {
            "if": {"properties": {"adt_type": {"const": "event"}}},
            "then": {
                "properties": {
                    "table": {"type": "integer"},
                    "select": select_schema,
                    "filter": filter_schema,
                    "aggregate": {"anyOf": [{"type": "null"},
                                  aggregate_schema]},
                    "postAggregateExpr": {"anyOf": [{"type": "null"},
                                          post_aggregate_schema]}
                },
                "required": ["table", "select"]
            }
        }
    ]
}

features_schema = {"type": "array", "items": feature_schema}

generated_features_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "date": {"type": "string", "format": "date"},
        "features": {"type": "object", "additionalProperties": True}
    },
    "required": ["id", "date", "features"]
}
