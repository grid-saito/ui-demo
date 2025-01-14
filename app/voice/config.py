tools_json = [
    {
        "type": "function",
        "function": {
            "name": "update_equipment_settings",
            "parameters": {
                "type": "object",
                "properties": {
                    "units": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "max_output": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                    "startup_cost": {
                        "type": "array",
                        "items": {"type": "integer"}
                    },
                },
                "required": ["units", "max_output", "startup_cost"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_objective_function",
            "parameters": {
                "type": "object",
                "properties": {
                    "objective": {
                        "type": "string",
                        "enum": ["Minimize Cost", "Maximize Output", "Balance Demand and Supply"],
                    },
                },
                "required": ["objective"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_constraints",
            "parameters": {
                "type": "object",
                "properties": {
                    "demand": {
                        "type": "integer",
                        "minimum": 500,
                        "maximum": 1500,
                    },
                    "max_output": {
                        "type": "integer",
                        "minimum": 100,
                        "maximum": 1000,
                    },
                },
                "required": ["demand", "max_output"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_optimization_methods",
            "parameters": {
                "type": "object",
                "properties": {
                    "methods": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["Genetic Algorithm", "Simulated Annealing", "Linear Programming"],
                        },
                    },
                },
                "required": ["methods"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_configuration",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
]