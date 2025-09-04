
import os
import sys
import yaml


importPath = os.path.normpath(
    os.path.dirname(os.path.realpath(os.path.abspath(__file__))) + "/.."
)

if not importPath in sys.path:
    sys.path.insert(1, importPath)


from check_schemata.checkProjectYAMLSchema import checkProjectYAMLSchema
from check_schemata.checkUserYAMLSchema import checkUserYAMLSchema


def evalOptionsRecord(projectOptionsDict, localOptionsDict):
    sendJobStartToken = True
    parserStartToken  = None
    parserEndToken    = None
    runtime           = None
    useCore			  = None
    useCoreName       = None
    useCoreUrl        = "dummy"

    # print(f"DEBUG: projectOptionsDict : {projectOptionsDict}")
    # print(f"DEBUG: localOptionsDict : {localOptionsDict}")


    if "SEND_JOB_START_TOKEN" in localOptionsDict:
        sendJobStartToken = localOptionsDict["SEND_JOB_START_TOKEN"]
    elif "SEND_JOB_START_TOKEN" in projectOptionsDict:
        sendJobStartToken = projectOptionsDict["SEND_JOB_START_TOKEN"]


    if "PARSER_START_TOKEN" in projectOptionsDict:
        parserStartToken = projectOptionsDict["PARSER_START_TOKEN"]


    if "PARSER_END_TOKEN" in projectOptionsDict:
        parserEndToken = projectOptionsDict["PARSER_END_TOKEN"]


    if "RUNTIME" in localOptionsDict:
        runtime = localOptionsDict["RUNTIME"]
    elif "RUNTIME" in projectOptionsDict:
        runtime = projectOptionsDict["RUNTIME"]

    if "USE_CORE" in localOptionsDict:
        useCore = localOptionsDict["USE_CORE"]
    elif "USE_CORE" in projectOptionsDict:
        useCore = projectOptionsDict["USE_CORE"]

    if useCore!= None:
        useCoreName = useCore["name"].lower()
        if useCoreName != "local":
            if "url" in useCore:
                useCoreUrl = useCore["url"]
            else:
                print(f"""FATAL: Must specify option "USE_CORE" with suboption "url" when using core "{useCoreName}" in project YAML !""")
    return sendJobStartToken, parserStartToken, parserEndToken, runtime, useCoreName, useCoreUrl
 

def readProjectYAML(project, user):
    with open(project, "r") as file:
        projectYAML = yaml.safe_load(file)

    # print(f"projectYAML : {projectYAML}\n")

    with open(user, "r") as file:
        userYAML = yaml.safe_load(file)

    # print(f"userYAML : {userYAML}\n")

    checkProjectYAMLSchema(projectYAML)
    checkUserYAMLSchema(userYAML)

    return (projectYAML, userYAML)


if __name__ == "__main__":

    (projectYAML, userYAML) = readProjectYAML(
        "config/project.yml",
        "config/user.yml",
    )

    evalOptionsRecord(projectYAML["options"], dict())

    exit(0)
