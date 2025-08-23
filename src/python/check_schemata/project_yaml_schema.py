from schema import And, Or, Use, Optional

projectYAMLSchema = {
    Optional("options"): {
                            Optional("SEND_JOB_START_TOKEN") : bool,
                            Optional("PARSER_START_TOKEN") : str,
                            Optional("PARSER_END_TOKEN") : str,
                            Optional("RUNTIME") : int,
                            Optional("USE_CORE") : {
                                                      "name": Or("local", str),
                                                      Optional("url"): And(str, lambda url: 'http' in url, error='\nERROR: "USE_CORE -> url" must contain "http"'),
                                                   },
                         },

# 'primes': [And(Or(int, float), error='\nERROR: "primes must be int or float')],
    
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
                  Optional("options"): {
                                          Optional("RUNTIME") : int,
                                          Optional("SEND_JOB_START_TOKEN") : bool,
                                       }
             } ]
    },

    Optional("unit-test"): {
        str: [ { 
                  "description": str,
                  "command": str,
                  "query": str,
                  "working_dir": str,
                  Optional("options"): {
                                          Optional("RUNTIME") : int,
                                          Optional("SEND_JOB_START_TOKEN") : bool,
                                       }
             } ]
    },
}
