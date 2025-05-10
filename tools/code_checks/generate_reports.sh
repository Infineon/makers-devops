#!/bin/bash

# Input directory containing results
RESULTS_DIR=$1

# Output HTML report directory
HTML_REPORT_DIR="${RESULTS_DIR}/html-report"
CLANG_TIDY_LOG_DIR=""
CPP_CHECK_REPORT_XML=""
MERGED_REPORT_XML="${RESULTS_DIR}/code-check.xml"

-rm -rf "${MERGED_REPORT_XML}"
-rm -rf "${HTML_REPORT_DIR}"
mkdir -p "${HTML_REPORT_DIR}"

# Check if cppcheck results exist
if [ -d "${RESULTS_DIR}/cppcheck" ]; then
  CPP_CHECK_REPORT_XML="${RESULTS_DIR}/cppcheck/check-cppcheck/check-cppcheck-errors.xml"
fi

# Check if clang-tidy results exist
if [ -d "${RESULTS_DIR}/clang-tidy" ]; then
  CLANG_TIDY_LOG_DIR="${RESULTS_DIR}/clang-tidy/check-clang-tidy"
fi

echo "Merging Code check reports ..."
  python3 extras/makers-devops/tools/code_checks/merge_clang_tidy_cppcheck.py \
    --logDir="${CLANG_TIDY_LOG_DIR}" \
    --xmlPath="${CPP_CHECK_REPORT_XML}" \
    --outputPath="${RESULTS_DIR}/code-check.xml"

echo "Generating HTML report ..."
cppcheck-htmlreport \
    --file="${RESULTS_DIR}/code-check.xml" \
    --title="Code Check Report" \
    --report-dir="${HTML_REPORT_DIR}" \
    --source-dir=.

# Final output
echo "Reports generated successfully."
