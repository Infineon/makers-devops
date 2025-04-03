
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

    exit(0)
