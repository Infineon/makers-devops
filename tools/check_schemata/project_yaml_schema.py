from schema import And, Or, Use, Optional

projectYAMLSchema = {
    Optional("compile"): {
        str: {
                "description": str,
                "command": str,
                "fqbns" : [str],
                "working_dir": str,
        }
    },
    
    Optional("code-quality"): {
        str: {
                "description": str,
                "command": str,
                "tool": str,
        }
    },

    Optional("example-test"): {
        str: [ { 
                  "description": str,
                  "command": str,
                  "query": str,
                  "working_dir": str,
             } ]
    },

    Optional("unit-test"): {
        str: [ { 
                  "description": str,
                  "command": str,
                  "query": str,
                  "working_dir": str,
             } ]
    },
    

}
