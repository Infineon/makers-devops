from schema import And, Or, Use, Optional

projectYAMLSchema = {
    Optional("build"): {
        str: {
                "description": str,
                "command": str,
                "working_dir": str,
        }
    },
    
    Optional("check"): {
        str: {
                "description": str,
                "command": str,
                "tool": str,
        }
    },

    Optional("example"): {
        str: [ { 
                  "description": str,
                  "command": str,
                  "query": str,
                  "working_dir": str,
             } ]
    },

    Optional("monitor"): {
        str: [ { 
                  "description": str,
                  "command": str,
                  "query": str,
                  "working_dir": str,
             } ]
    },
    

}
