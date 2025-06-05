import os
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse

def create_results_xml(file_path):
    """
    This function is used to initialize the XML file where code check results will be appended.
    It creates an XML file with a root element named "results" and a version attribute set to "2".
    
    Args:
        file_path (str): The path where the XML file will be created.
    """
    # Create the root element
    root = ET.Element("results")
    root.set("version", "2")

    # Create an ElementTree object from the root
    tree = ET.ElementTree(root)

    # Write the XML to the specified file with the proper declaration
    with open(file_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

def append_code_check_xml_to_results_xml(output_xml_path, xml_file):
    tree = ET.parse(output_xml_path)
    root = tree.getroot()
    xml_tree = ET.parse(xml_file)
    xml_root = xml_tree.getroot()

    for child in xml_root:
        root.append(child)

    # Write back the updated results.xml
    tree.write(output_xml_path, encoding="utf-8", xml_declaration=True)

def parse_clang_tidy_log(file_path):
    errors = []
    with open(file_path, "r") as file:
        content = file.read()

    # Regular expressions to match errors and warnings
    pattern = re.compile(r"(?P<type>error|warning): (?P<msg>.+?) \[(?P<id>[\w\-]+)\]")
    location_pattern = re.compile(r"(.+?):(\d+):(\d+):")

    for match in pattern.finditer(content):
        location_match = location_pattern.search(content, match.start())
        if location_match:
            file_path, line, column = location_match.groups()
            errors.append(
                {
                    "type": match.group("type"),
                    "msg": match.group("msg"),
                    "id": match.group("id"),
                    "file": file_path,
                    "line": line,
                    "column": column,
                }
            )

    return errors


def append_clang_tidy_results_to_xml(output_xml_path, clang_tidy_results):
    tree = ET.parse(output_xml_path)
    root = tree.getroot()

    # Check if clang-tidy section exists, else create it
    clang_tidy_section = root.find("clang-tidy")
    if clang_tidy_section is None:
        clang_tidy_section = ET.SubElement(root, "clang-tidy", version="2.17 dev")
        ET.SubElement(clang_tidy_section, "errors")

    errors_section = clang_tidy_section.find("errors")
    existing_errors = set()

    for result in clang_tidy_results:
        unique_id = (
            result["file"],
            result["line"],
            result["column"],
            result["msg"],
            result["type"],
            "clang-tidy-" + result["id"],
        )
        if unique_id not in existing_errors:
            existing_errors.add(unique_id)
            error_element = ET.SubElement(
                errors_section,
                "error",
                {
                    "id": "clang-tidy-" + result["id"],
                    "severity": result["type"],
                    "msg": result["msg"],
                    "verbose": result["msg"],
                },
            )
            location_element = ET.SubElement(
                error_element,
                "location",
                {
                    "file": result["file"],
                    "line": result["line"],
                    "column": result["column"],
                },
            )

    # Pretty-print the XML
    xml_str = ET.tostring(root, encoding="unicode")
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    with open(output_xml_path, "w") as file:
        file.write(pretty_xml_str)


def main(clang_tidy_log_dir, cppcheck_xml_path, output_xml_path):
    create_results_xml(output_xml_path)

    if cppcheck_xml_path != "":
        append_code_check_xml_to_results_xml(output_xml_path, cppcheck_xml_path)
        
    if clang_tidy_log_dir != "":
        clang_tidy_results = []

        for log_file in os.listdir(clang_tidy_log_dir):
            if log_file.endswith(".log"):
                log_path = os.path.join(clang_tidy_log_dir, log_file)
                results = parse_clang_tidy_log(log_path)
                clang_tidy_results.extend(results)

        append_clang_tidy_results_to_xml(output_xml_path, clang_tidy_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse clang-tidy logs and append results to cppcheck XML file."
    )
    parser.add_argument(
        "--logDir",
        type=str,
        default="",
        help="Directory containing clang-tidy log files.",
    )
    parser.add_argument(
        "--xmlPath",
        type=str,
        default="",
        help="Path to the cppcheck XML file.",
    )
    parser.add_argument(
        "--outputPath",
        type=str,
        required=True,
        help="Path to the output XML file to append results.",
    )
    args = parser.parse_args()
    main(args.logDir, args.xmlPath, args.outputPath)

