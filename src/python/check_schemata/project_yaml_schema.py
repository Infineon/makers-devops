from schema import And, Or, Use, Optional

projectYAMLSchema = {
    Optional("options"): {
                            Optional("USE_CORE") : { 
                                                     "name": Or("local", str),
                                                     Optional("url"): And(str, lambda url: 'http' in url, error='\nERROR: "USE_CORE -> url" must contain "http"'),
                            },
    },
# configSchema = {
#                 'rest': {
#                             'url' : And(str, lambda url: 'http' in url, error='\nERROR: "rest -> url" must contain "http"'),
#                             'port': int
#                 },

#                 'primes': [And(Or(int, float), error='\nERROR: "primes must be int or float')],
#             }
    
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
                  Optional("options"): { str : str }
             } ]
    },

    Optional("unit-test"): {
        str: [ { 
                  "description": str,
                  "command": str,
                  "query": str,
                  "working_dir": str,
                  Optional("options"): Or( None,
                                        #    And(
                                               {
                                                    Optional("SEND_JOB_START_TOKEN") : bool,
                                                    Optional("PARSE_START_TOKEN") : str,
                                                    Optional("PARSE_END_TOKEN") : str,
                                                    Optional("USE_CORE") : { 
                                                                              "name": Or("local", str),
                                                                              Optional("url"): str,
                                                    },
                                               }
                                        #    )
                  )
             } ]
    },
    

}
