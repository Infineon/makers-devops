from schema import And, Or, Use, Optional

userYAMLSchema = {
    Optional("compile"): [And(str)],
    Optional("code-quality"): [And(str)],
    Optional("example-test"): [And(str)],
    Optional("unit-test"): [And(str)],
}
