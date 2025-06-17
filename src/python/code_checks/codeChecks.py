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

    # parser.add_argument(
    #     "--runAllHILChecks", action="store_true", help="Run all HIL checks."
    # )
    
    parser.add_argument("--runCheck", type=str, help="Run a specific check.")
   
    parser.add_argument("--runCheckIndex", type=int, default=0, help="Run the check at the specified index (starting from 0, default 0) in the list of checks if multiple are specified for the check.")
    
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


def runCheck(projectYAML, checkType=None, check=None, checkIndex=0):
    returnCode = 0
    currentReturnCode = 0
    failedJobs = []
    passedJobs = []
    
    if checkType is None:
        print(f"ERROR : Check type 'None' is not valid !")
        returnCode = 1

    elif check is None:
        print(f"ERROR : Check 'None' is not valid !")
        returnCode = 1

    elif checkType == "compile":
        for fqbn in projectYAML[checkType][check]['fqbns']:
            currentReturnCode |= subprocess.run(
                [
                    "extras/makers-devops/bin/run_command.sh",
                    "-w", f"{projectYAML[checkType][check]['working_dir']}",
                    "-c", f"{projectYAML[checkType][check]['command']} FQBN={fqbn}",
                ]
            ).returncode

            returnCode |= currentReturnCode

            if currentReturnCode != 0:
                failedJobs.append(check)
            else:
                passedJobs.append(check)

        for job in failedJobs:
            print(f"ERROR : Job '{check}' failed !")

        for job in passedJobs:
            print(f"ERROR : Job '{check}' passed !")


    elif checkType == "code-quality":
        # if "command" not in projectYAML[checkType][check]:
        #     print(
        #         f"ERROR : Option 'command' not found in project YAML for {checkType} / {check} !"
        #     )
        #     returnCode = 1

        # else:
        paramList = projectYAML[checkType][check]["command"].split()
        paramList.insert(1, f"--file-prefix={check}")
        currentReturnCode |= subprocess.run(paramList).returncode

        if currentReturnCode != 0:
            print(f"ERROR: Job '{check}' failed !")
        else:
            print(f"INFO: Job '{check}' passed !")


    elif checkType == "example-test":
        currentReturnCode |= subprocess.run(
            [
                "extras/makers-devops/bin/run_command.sh",
                "-w", f"{projectYAML[checkType][check][checkIndex]['working_dir']}",
                "-c", f"{projectYAML[checkType][check][checkIndex]['command']} FQBN={args.fqbn} PORT={args.port}",
            ]
        ).returncode

        returnCode |= currentReturnCode

        if currentReturnCode != 0:
            print(f"ERROR: Job '{check}' failed !")
        else:
            print(f"INFO: Job '{check}' passed !")

    elif checkType == "unit-test":
        currentReturnCode |= subprocess.run(
            [
                "extras/makers-devops/bin/run_command.sh",
                "-w", f"{projectYAML[checkType][check][checkIndex]['working_dir']}",
                "-c", f"{projectYAML[checkType][check][checkIndex]['command']} FQBN={args.fqbn} PORT={args.port}",
            ]
        ).returncode

        returnCode |= currentReturnCode

        if currentReturnCode != 0:
            print(f"ERROR: Job '{check}' failed !")
        else:
            print(f"INFO: Job '{check}' passed !")


    if returnCode != 0:
        print(f"ERROR : Some check(s) failed, please check logfile !")
 
    return returnCode


if __name__ == "__main__":
    returnCode = 0
    args = parseArgs()

    (projectYAML, userYAML) = readProjectYAML(
        os.getcwd() + "/" + args.projectYAML, os.getcwd() + "/" + args.userYAML
    )

    if args.runAllCodeChecks or args.runCheck:
        if "options" in projectYAML:
            options =  projectYAML["options"]

            if "USE_CORE" in options:
                useCore = options["USE_CORE"]

                if "local" in useCore:
                    returnCode |= subprocess.run(
                        [
                            "extras/makers-devops/bin/install_arduino_core.sh",
                            "-c", "local"
                        ]
                    ).returncode
                else:
                    coreName = useCore["name"]

                    if "url" not in useCore:
                        print(f"When specifying a specific core an Url must also be specified !\n")
                        exit(1)
                    else:
                        returnCode |= subprocess.run(
                            [
                                "extras/makers-devops/bin/install_arduino_core.sh",
                                "-c", coreName,
                                "-u", useCore["url"],
                            ]
                        ).returncode
                    



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

    # if args.runAllHILChecks:
    #     for checkType, checkTypeList in userYAML.items():
    #         if checkType not in projectYAML:
    #             print(f"ERROR : Check type '{checkType}' not found in project YAML !")
    #             returnCode = 1

    #         elif checkType in ['example-test', 'unit-test']:
    #             for check in checkTypeList:
    #                 if check not in projectYAML[checkType]:
    #                     print(
    #                         f"ERROR : Check '{check}' not found in project YAML for check type '{checkType}' !"
    #                     )
    #                     returnCode = 1
    #                 else:
    #                     returnCode |= runCheck(projectYAML, checkType, check)

    elif args.runCheck:
        check = args.runCheck
        checkIndex = args.runCheckIndex
        type = None

        for checkType, checkTypeList in userYAML.items():
            if check in checkTypeList:
                type = checkType
                break

        returnCode |= runCheck(projectYAML, type, check, checkIndex)

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
