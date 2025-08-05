#!/bin/bash


echo "executing $0 ..."

usage() {
  echo "Usage: $0 [-s | --source] <source repo folder> [-d | --destination] <remote destination folder> [--remote] <user@machine> [-h | --help]" 1>&2
  echo "Optional parameters:" 1>&2
  echo "  --projectYAML <path>  Path to project YAML file (default: config/project.yml)" 1>&2
  echo "  --userYAML <path>     Path to user YAML file (default: config/user.yml)" 1>&2
  echo "  --skip-copy           Skip copying source folder to remote destination." 1>&2
  echo "Notes:" 1>&2
  echo "  - All paths (source, destination) must be absolute paths." 1>&2
  echo "  - Remote user and machine must be in the format 'user@machine'." 1>&2
  exit 1
}

# Default values for optional parameters
project_yaml="config/project.yml"
user_yaml="config/user.yml"

# Parse options
TEMP=$(getopt -o s:d:h --long source:,destination:,remote:,help,projectYAML:,userYAML:,skip-copy -n "$0" -- "$@")
if [ $? != 0 ]; then
  echo "Terminating..." >&2
  usage
fi

# Evaluate parsed options
eval set -- "$TEMP"

source_folder=""
destination=""
remote_user_machine=""
skip_copy=false

while true; do
  case "$1" in
    -s | --source )      source_folder=$2; shift 2 ;;
    -d | --destination ) destination=$2; shift 2 ;;
         --remote )      remote_user_machine=$2; shift 2 ;;
    -h | --help )        usage ;;
         --projectYAML ) project_yaml=$2; shift 2 ;;
         --userYAML )    user_yaml=$2; shift 2 ;;
         --skip-copy )   skip_copy=true; shift ;;
         -- )            shift; break ;;
    * )                  echo "Unknown option '$1' found!" ; usage ;;
  esac
done

if [ -z "$source_folder" ] || [ -z "$destination" ] || [ -z "$remote_user_machine" ]; then
  usage
fi

# Check if source folder exists
if [ ! -d "$source_folder" ]; then
  echo "ERROR: Source folder '$source_folder' does not exist!" >&2
  exit 1
fi

PARENT_DIR_SOURCE=$(dirname "$source_folder")
BASE_NAME_SOURCE=$(basename "$source_folder")

PARENT_DIR_DEST=$(dirname "$destination")
BASE_NAME_DEST=$(basename "$destination")

# Check if base names are the same
if [ "$BASE_NAME_SOURCE" != "$BASE_NAME_DEST" ]; then
  echo "ERROR: Source folder base name '$BASE_NAME_SOURCE' and destination base name '$BASE_NAME_DEST' do not match!" >&2
  exit 1
fi

# Copy source folder to remote if --skip-copy is not provided
if [ "$skip_copy" = false ]; then
  echo "Copying $source_folder to $remote_user_machine:$destination ..."
  ssh "$remote_user_machine" "rm -rf $destination && mkdir -p $destination" || {
    echo "Failed to prepare remote destination folder!" >&2
    exit 1
  }

  cd $PARENT_DIR_SOURCE
  tar -czf - -C "$PARENT_DIR_SOURCE" "$BASE_NAME_SOURCE" | ssh "$remote_user_machine" "tar -xpzf - -C $PARENT_DIR_DEST --checkpoint=1000 --checkpoint-action=dot" || {
    echo "Failed to copy folder to remote destination!" >&2
    exit 1
  }
else
  # Adjust project_yaml path based on destination
  project_yaml_path="$destination/$project_yaml"
  user_yaml_path="$destination/$user_yaml"

  echo "Checking if destination folder and config files exist on remote..."
  ssh "$remote_user_machine" "[ -d $destination ] && [ -f $project_yaml_path ] && [ -f $user_yaml_path ]" || {
    echo "ERROR: Destination folder or config files do not exist on remote!" >&2
    exit 1
  }
fi

echo "Switching to remote operations..."
ssh "$remote_user_machine" <<EOF
  echo "Changing to destination directory: $destination"
  cd $destination

  echo "Fetching HIL checks from codeChecks.py..."
  raw_output=\$(python3 extras/makers-devops/src/python/code_checks/codeChecks.py --projectYAML "$project_yaml" --userYAML "$user_yaml" --getAllHILChecks)
  matrix_checks=\$(echo "\$raw_output" |  sed -n 's/^echo "checks=\(.*\)" >>.*$/\1/p' | sed 's/\\"/"/g' | tr -d '\\')


  if [ \$? -ne 0 ]; then
    echo "ERROR: Failed to fetch HIL checks!" >&2
    exit 1
  fi

  echo "HIL checks fetched successfully:"
  echo "\$matrix_checks"

  processed_checks=\$(echo "\$matrix_checks" | sed 's/[][]//g' | tr -d '"' | tr ',' '\n')
  echo "Running hilChecks.py for each check..."
  echo "\$processed_checks" | while read -r check; do
      echo "Running hilChecks.py for check: \$check"
      hilChecks.py --projectYAML "$project_yaml" --userYAML "$user_yaml" --runCheck "\$check" --dockerTag=latest 2>&1 | tee /tmp/hilChecks_output.log

      # Extract and display the summary
      awk '/Summary/,/Switching off HIL devices/' /tmp/hilChecks_output.log 

      if [ \$? -ne 0 ]; then
        echo "ERROR: hilChecks.py execution failed for check: \$check" >&2
        exit 1
      fi
  done
EOF

exit $?