#!/bin/bash

echo ""
echo "Executing $* ..."

usage() {
  echo "Usage: $0 [--results-dir] <Results directory> [--merge-script] <Path to merge script> [--source-dir] <Source directory>" 1>&2
  exit 1
}

TEMP=`getopt -o r:m:s: --long results-dir:,merge-script:,source-dir: -n "$0" -- "$@"`
if [ $? != 0 ]; then
  echo "Terminating..." >&2
  usage
  exit 1
fi

eval set -- "$TEMP"

results_dir=""
merge_script="extras/makers-devops/src/python/code_checks/merge_clang_tidy_cppcheck.py"
source_dir="."

while true; do
  case "$1" in
    --results-dir ) results_dir=$2; shift 2 ;;
    --merge-script ) merge_script=$2; shift 2 ;;
    --source-dir ) source_dir=$2; shift 2 ;;
    -- ) shift; break ;;
    * ) echo "Unknown option '$1' found!"; usage; break ;;
  esac
done

if [ -z "$results_dir" ]; then
  echo "Error: --results-dir is required."
  usage
fi

html_report_base_dir="${results_dir}/html-reports"
mkdir -p "${html_report_base_dir}"

echo ""
echo "results-dir        : $results_dir"
echo "merge-script       : $merge_script"
echo "source-dir         : $source_dir"
echo ""

# Collect cppcheck XML files and clang-tidy directories into arrays
declare -A cppcheck_reports
declare -A clang_tidy_reports

# Find cppcheck XML files for each group (source, library, test, etc.)
if [ -d "${results_dir}/cppcheck" ]; then
  for file in $(find "${results_dir}/cppcheck" -name "*.xml"); do
    group=$(basename "$(dirname "${file}")" | sed -E 's/-cppcheck.*//') # Extract group name (e.g., source, examples, test)
    cppcheck_reports["${group}"]="${cppcheck_reports[${group}]} ${file}"
  done
fi

# Find clang-tidy directories for each group
if [ -d "${results_dir}/clang-tidy" ]; then
  for dir in $(find "${results_dir}/clang-tidy" -type d -name "*-clang-tidy"); do
    group=$(basename "${dir}" | sed -E 's/-clang-tidy//') # Extract group name (e.g., source, library, test)
    clang_tidy_reports["${group}"]="${clang_tidy_reports[${group}]} ${dir}"
  done
fi

# Check if any reports are found
if [ ${#cppcheck_reports[@]} -eq 0 ] && [ ${#clang_tidy_reports[@]} -eq 0 ]; then
  echo "Error: No cppcheck or clang-tidy reports found in ${results_dir}. Exiting."
  exit 1
fi

# Print collected tool reports for debugging
echo "Found cppcheck reports:"
for group in "${!cppcheck_reports[@]}"; do
  echo "  ${group}: ${cppcheck_reports[$group]}"
done

echo "Found clang-tidy reports:"
for group in "${!clang_tidy_reports[@]}"; do
  echo "  ${group}: ${clang_tidy_reports[$group]}"
done

# Process each group and generate reports
for group in "${!cppcheck_reports[@]}" "${!clang_tidy_reports[@]}"; do
  merged_report_xml="${results_dir}/${group}-code-check.xml"
  html_report_dir="${html_report_base_dir}/${group}"

  cppcheck_xml_files=${cppcheck_reports[$group]}
  clang_tidy_dirs=${clang_tidy_reports[$group]}

  echo "Processing group: ${group}"
  echo "  cppcheck reports: ${cppcheck_xml_files}"
  echo "  clang-tidy directories: ${clang_tidy_dirs}"

  # Merge reports using the Python script
  if [ ! -f "${merge_script}" ]; then
    echo "Error: Merge script not found at ${merge_script}. Exiting."
    exit 1
  fi

  echo "Merging tool reports for group '${group}' into a single XML..."
  python3 "${merge_script}" \
    --logDir="$(echo ${clang_tidy_dirs} | tr ' ' ',')" \
    --xmlPath="$(echo ${cppcheck_xml_files} | tr ' ' ',')" \
    --outputPath="${merged_report_xml}"

  # Generate HTML report for this group
  echo "Generating HTML report for group '${group}'..."
  mkdir -p "${html_report_dir}"
  cppcheck-htmlreport \
    --file="${merged_report_xml}" \
    --title="Code Check Report - ${group}" \
    --report-dir="${html_report_dir}" \
    --source-dir="${source_dir}"

  echo "HTML report for group '${group}' available at: ${html_report_dir}"
done

# Set permissions
chown -R --reference=. "${html_report_base_dir}"

echo "$0 done."
exit 0