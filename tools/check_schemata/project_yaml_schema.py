from schema import And, Or, Use, Optional

projectYAMLSchema = {
    Optional("build"): {
        str: {
            "description": str,
            "target": str,
            "fqbn": str,
        }
    },
    
    Optional("check"): {
        str: {
            "description": str,
            "tool": str,
            "command": str,
        }
    },
}
