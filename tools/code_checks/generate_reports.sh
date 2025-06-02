#!/bin/bash

set -e

RESULTS_DIR=$1
if [ -z "${RESULTS_DIR}" ]; then
  echo "Error: RESULTS_DIR not provided. Please provide the results directory as the first argument."
  exit 1
fi

HTML_REPORT_DIR="${RESULTS_DIR}/html-report"
MERGED_REPORT_XML="${RESULTS_DIR}/code-check.xml"

# Clean up previous reports
rm -rf "${MERGED_REPORT_XML}" "${HTML_REPORT_DIR}"
mkdir -p "${HTML_REPORT_DIR}"

# variables for various tool reports
declare -A TOOL_XML_REPORTS

# Search for cppcheck results
if [ -d "${RESULTS_DIR}/cppcheck" ]; then
  CPP_CHECK_REPORT_XML=$(find "${RESULTS_DIR}/cppcheck" -name "*.xml" | head -n 1)
  if [ -n "${CPP_CHECK_REPORT_XML}" ]; then
    TOOL_XML_REPORTS["cppcheck"]="${CPP_CHECK_REPORT_XML}"
  fi
fi

# Search for clang-tidy results
if [ -d "${RESULTS_DIR}/clang-tidy" ]; then
  CLANG_TIDY_LOG_DIR=$(find "${RESULTS_DIR}/clang-tidy" -name "code-quality-clang-tidy" -type d | head -n 1)
  if [ -n "${CLANG_TIDY_LOG_DIR}" ]; then
    TOOL_XML_REPORTS["clang-tidy"]="${CLANG_TIDY_LOG_DIR}"
  fi
fi

# Check if any reports are found
if [ ${#TOOL_XML_REPORTS[@]} -eq 0 ]; then
  echo "Error: No cppcheck or clang-tidy reports found in ${RESULTS_DIR}. Exiting."
  exit 1
fi

# Print collected tool reports for debugging
echo "Found the following tool reports:"
for tool in "${!TOOL_XML_REPORTS[@]}"; do
  echo "  ${tool}: ${TOOL_XML_REPORTS[$tool]}"
done

# Merge reports using a Python script
echo "Merging tool reports into a single XML..."
MERGE_SCRIPT="extras/makers-devops/tools/code_checks/merge_clang_tidy_cppcheck.py"
if [ ! -f "${MERGE_SCRIPT}" ]; then
  echo "Error: Merge script not found at ${MERGE_SCRIPT}. Exiting."
  exit 1
fi

python3 "${MERGE_SCRIPT}" \
  --logDir="${TOOL_XML_REPORTS["clang-tidy"]}" \
  --xmlPath="${TOOL_XML_REPORTS["cppcheck"]}" \
  --outputPath="${MERGED_REPORT_XML}"

# Generate HTML report
echo "Generating HTML report..."
cppcheck-htmlreport \
  --file="${MERGED_REPORT_XML}" \
  --title="Code Check Report" \
  --report-dir="${HTML_REPORT_DIR}" \
  --source-dir=.

# Final output
echo "Reports generated successfully. HTML report available at: ${HTML_REPORT_DIR}"
