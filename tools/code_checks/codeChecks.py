#!/usr/bin/python3

# python3 codeChecks.py

import argparse
import subprocess
import sys
import os

tools_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, tools_path + "/..")

from project_yaml.readProjectYAML import readProjectYAML


def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--getAllCodeChecks", action="store_true", help="Get all code checks."
    )

    parser.add_argument(
        "--getAllHILChecks", action="store_true", help="Get all HIL checks."
    )

    parser.add_argument(
        "--runAllCodeChecks", action="store_true", help="Run all code checks."
    )

    parser.add_argument(
        "--runAllHILChecks", action="store_true", help="Run all HIL checks."
    )
    
    parser.add_argument("--runCheck", type=str, help="Run a specific check.")
    
    parser.add_argument(
        "--projectYAML", type=str, required=True, help="Path to the project YAML file."
    )
    parser.add_argument(
        "--userYAML", type=str, required=True, help="Path to the user YAML file."
    )
    
    parser.add_argument(
        "--fqbn", type=str, required=False, help="FQBN of device to be compiled or tested."
    )
    parser.add_argument(
        "--port", type=str, required=False, help="Port of device to be compiled or tested."
    )

    args = parser.parse_args()

    return args


def runCheck(projectYAML, checkType=None, check=None):
    returnCode = 0

    if checkType is None:
        print(f"ERROR : Check type 'None' is not valid !")
        returnCode = 1

    elif check is None:
        print(f"ERROR : Check 'None' is not valid !")
        returnCode = 1

    elif checkType == "compile":
        returnCode |= subprocess.run(
            [
                "extras/makers-devops/bin/run_command.sh",
                "-w", f"{projectYAML[checkType][check]['working_dir']}",
                "-c", f"{projectYAML[checkType][check]['command']}",
            ]
        ).returncode
        # returnCode |= subprocess.run(
        #     [
        #         "make",
        #         "run-build-target",
        #         f"FQBN={projectYAML[checkType][check]['fqbn']}",
        #         f"TARGET={projectYAML[checkType][check]['target']}",
        #     ]
        # ).returncode

    elif checkType == "code-quality":
        if "command" not in projectYAML[checkType][check]:
            print(
                f"ERROR : Option 'command' not found in project YAML for {checkType} / {check} !"
            )
            returnCode = 1

        else:
            paramList = projectYAML[checkType][check]["command"].split()
            paramList.insert(1, f"--file-prefix={check}")
            returnCode |= subprocess.run(paramList).returncode

    # TODO: list element 0 used !
    elif checkType == "example-test":
        returnCode |= subprocess.run(
            [
                "extras/makers-devops/bin/run_command.sh",
                "-w", f"{projectYAML[checkType][check][0]['working_dir']}",
                "-c", f"{projectYAML[checkType][check][0]['command']} FQBN={args.fqbn} PORT={args.port}",
            ]
        ).returncode

    # TODO: list element 0 used !
    elif checkType == "unit-test":
        returnCode |= subprocess.run(
            [
                "extras/makers-devops/bin/run_command.sh",
                "-w", f"{projectYAML[checkType][check][0]['working_dir']}",
                "-c", f"{projectYAML[checkType][check][0]['command']} FQBN={args.fqbn} PORT={args.port}",
            ]
        ).returncode

    if returnCode == 2:
        print(f"ERROR : Running check '{check}' failed due to failed code checks !")
    elif returnCode != 0:
        print(f"ERROR : Problem running check '{check}' !")

    return returnCode


if __name__ == "__main__":
    returnCode = 0
    args = parseArgs()

    (projectYAML, userYAML) = readProjectYAML(
        os.getcwd() + "/" + args.projectYAML, os.getcwd() + "/" + args.userYAML
    )

    if args.runAllCodeChecks:
        for checkType, checkTypeList in userYAML.items():
            if checkType not in projectYAML:
                print(f"ERROR : Check type '{checkType}' not found in project YAML !")
                returnCode = 1

            elif checkType in ['compile', 'code-quality']:
                for check in checkTypeList:
                    if check not in projectYAML[checkType]:
                        print(
                            f"ERROR : Check '{check}' not found in project YAML for check type '{checkType}' !"
                        )
                        returnCode = 1
                    else:
                        returnCode |= runCheck(projectYAML, checkType, check)

    if args.runAllHILChecks:
        for checkType, checkTypeList in userYAML.items():
            if checkType not in projectYAML:
                print(f"ERROR : Check type '{checkType}' not found in project YAML !")
                returnCode = 1

            elif checkType in ['example-test', 'unit-test']:
                for check in checkTypeList:
                    if check not in projectYAML[checkType]:
                        print(
                            f"ERROR : Check '{check}' not found in project YAML for check type '{checkType}' !"
                        )
                        returnCode = 1
                    else:
                        returnCode |= runCheck(projectYAML, checkType, check)

    elif args.runCheck:
        check = args.runCheck
        type = None

        for checkType, checkTypeList in userYAML.items():
            if check in checkTypeList:
                type = checkType
                break

        returnCode |= runCheck(projectYAML, type, check)

    elif args.getAllCodeChecks:
        allChecks = 'echo "checks=['

        for checkType, checkTypeList in userYAML.items():
            if checkType not in projectYAML:
                print(f"ERROR : Check type '{checkType}' not found in project YAML !")
                returnCode = 1

            elif checkType in ['compile', 'code-quality']:
                for check in checkTypeList:
                    if check not in projectYAML[checkType]:
                        print(
                            f"ERROR : Check '{check}' not found in project YAML for check type '{checkType}' !"
                        )
                        returnCode = 1
                    else:
                        allChecks += f'\\"{check}\\",'

        allChecks += ']" >> "$GITHUB_OUTPUT"'
        allChecks = allChecks.replace(",]", "]")

        print(f"{allChecks}")

    elif args.getAllHILChecks:
        allChecks = 'echo "checks=['

        for checkType, checkTypeList in userYAML.items():
            if checkType not in projectYAML:
                print(f"ERROR : Check type '{checkType}' not found in project YAML !")
                returnCode = 1

            elif checkType in ['example-test', 'unit-test']:
                for check in checkTypeList:
                    if check not in projectYAML[checkType]:
                        print(
                            f"ERROR : Check '{check}' not found in project YAML for check type '{checkType}' !"
                        )
                        returnCode = 1
                    else:
                        allChecks += f'\\"{check}\\",'

        allChecks += ']" >> "$GITHUB_OUTPUT"'
        allChecks = allChecks.replace(",]", "]")

        print(f"{allChecks}")

    else:
        print(f"\nERROR : Wrong parameters passed !\n")
        returnCode = 1

    exit(returnCode)
