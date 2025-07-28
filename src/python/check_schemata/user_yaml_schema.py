from schema import And, Or, Use, Optional

userYAMLSchema = {
    Optional("compile"): [str],
    Optional("code-quality"): [str],
    Optional("example-test"): [str],
    Optional("unit-test"): [str],
}
