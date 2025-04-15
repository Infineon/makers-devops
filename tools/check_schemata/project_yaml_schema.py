from schema import And, Or, Use, Optional

projectYAMLSchema = {
    Optional("build"): {
        str: {
                "description": str,
                "target": str,
                "fqbn": str,
                "working_dir": str,
        }
    },
    
    Optional("check"): {
        str: {
                "description": str,
                "tool": str,
                "command": str,
        }
    },

    Optional("hil"): {
        str: [ { 
                  "description": str,
                  "target": str,
                  "query": str,
                  "working_dir": str,
             } ]
    },
    

}
