#!/bin/sh

echo "Environment variables :"
echo "    ARDUINO_CLI_VERSION  : ${ARDUINO_CLI_VERSION}"
echo "    XMC4ARDUINO_VERSION  : ${XMC4ARDUINO_VERSION}"
echo "    PSOC4ARDUINO_VERSION : ${PSOC4ARDUINO_VERSION}"
echo ""

echo "Tools :"
echo "    which arduino-cli : "`which arduino-cli`
echo ""

echo "    clang --version : "`clang --version`
echo ""

echo "    clang-format --version : "`clang-format --version`
echo ""

echo "    clang-tidy --version : "`clang-tidy --version`
echo ""

echo "    gcc --version : "`gcc --version`
echo ""

echo "    cppcheck --version : "`cppcheck --version`
echo ""

echo "    which scanbuild : "`which scanbuild`
echo ""
