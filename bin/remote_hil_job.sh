#!/bin/bash

# Prepend makers-hil/bin and makers-hil/src/python/hil to PATH
export PATH="$(dirname "$0")/../../../makers-hil/bin:$(dirname "$0")/../../../makers-hil/src/python/hil:$PATH"
# remote_hil_job.sh
# Usage: remote_hil_job.sh <destination> <project_yaml> <user_yaml>

set -e

destination="$1"
project_yaml="$2"
user_yaml="$3"

cd "$destination"

echo "Fetching HIL checks from codeChecks.py..."
raw_output=$(python3 extras/makers-devops/src/python/code_checks/codeChecks.py --projectYAML "$project_yaml" --userYAML "$user_yaml" --getAllHILChecks)
matrix_checks=$(echo "$raw_output" |  sed -n 's/^echo "checks=\(.*\)" >>.*$/\1/p' | sed 's/\\"/"/g' | tr -d '\\')

if [ $? -ne 0 ]; then
  echo "ERROR: Failed to fetch HIL checks!" >&2
  exit 1
fi

echo "HIL checks fetched successfully:"
echo "$matrix_checks"

processed_checks=$(echo "$matrix_checks" | sed 's/[][]//g' | tr -d '"' | tr ',' '\n')
echo "Running hilChecks.py for each check..."
output_log=$(mktemp "hilChecks_output.XXXXXX.log")

> "$output_log"
echo "$processed_checks" | while read -r check; do
    echo "Running hilChecks.py for check: $check"
    hilChecks.py --projectYAML "$project_yaml" --userYAML "$user_yaml" --runCheck "$check" --dockerTag=latest 2>&1 | tee -a "$output_log"

    if [ $? -ne 0 ]; then
      echo "ERROR: hilChecks.py execution failed for check: $check" >&2
      exit 1
    fi
done

echo "Extracting and calculating test results..."
awk -v matrix_checks="$matrix_checks" '
/^response/ { next }
  /^===== Check:/ {
      print "\n" $0
      next
  }
  /^Unity test run/ || /^TEST\(/ || (/[0-9]+ Tests [0-9]+ Failures [0-9]+ Ignored/ ) || /^OK$/ || /^FAIL$/ {
    print
  }
  /[0-9]+ Tests [0-9]+ Failures [0-9]+ Ignored/{
      total_tests += $1
      failed_tests += $3
      ignored_tests += $5
  }
  END {
      print "=============================="
      print "      Test Summary Report     "
      print "=============================="
      print "Matrix Checks: " matrix_checks
      print "------------------------------"
      print "Total number of tests   : " total_tests
      print "Total number of failed  : " failed_tests
      print "Total number of ignored : " ignored_tests
      print "=============================="
  }' "$output_log"
echo "[INFO] Output log stored at: $output_log"
