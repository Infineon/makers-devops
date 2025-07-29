# Testing

This document contains the project code testing guidelines. It should answer any
questions you may have as an aspiring contributor.

## Test suites

This project has one test suite for testing:

* Unit tests - located in the test/unit subdirectory. Tests are based on [Unity](https://www.throwtheswitch.org/unity), assertions and a dedicated makefile for executing the tests. Unit tests should be fast and test only the module as specified by the [naming convention](README.md#test-naming-convention).


## Writing new tests

Most code changes will fall into one of the following categories.

### Writing tests for new features

New code should be covered by unit tests. If the code is difficult to test with
unit tests, then that is a good sign that it should be refactored to make it
easier to reuse and maintain. Consider accepting unexported interfaces instead
of structs so that fakes can be provided for dependencies.

If the new feature includes a completely new API endpoint then a new API
integration test should be added to cover the success case of that endpoint.

If the new feature does not include a completely new API endpoint consider
adding the new API fields to the existing test for that endpoint. A new
integration test should **not** be added for every new API field or API error
case. Error cases should be handled by unit tests.

### Writing tests for bug fixes

Bugs fixes should include a unit test case which exercises the bug.

A bug fix may also include new assertions in existing integration tests for the
API endpoint.


## Running tests

### Unit Tests

To run the unit test suite:

```
make test-unit
```

or `hack/test/unit` from inside a `BINDDIR=. make shell` container or properly
configured environment.

The following environment variables may be used to run a subset of tests:

* `TESTDIRS` - paths to directories to be tested, defaults to `./...`
* `TESTFLAGS` - flags passed to `go test`, to run tests which match a pattern
  use `TESTFLAGS="-test.run TestNameOrPrefix"`

### Arduino-CLI Version

You can change a version of arduino-cli used for building and testing by specifying the  `ARDUINO-CLI-VERSION` variable when invoking the makefile, for example:

```
make ARDUINO-CLI-VERSION=1.12.8 test
```
