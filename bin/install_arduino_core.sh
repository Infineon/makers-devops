#!/bin/bash


echo "executing $0 $* ..."


usage() {
  echo "Usage: $0 :" 1>&2;
  echo "          [-c | --core] <Core to be installed.>   [-u | --url] <Url to download core.>" 1>&2;
#  echo "          [-c | --core] <Core to be installed.>   [-l | --local] <Install local core package in Arduino.>   [-u | --url] <Url to download core.>   [-w | --working_dir] <Container working directory.>" 1>&2;
  exit 1;
}


# This requires GNU getopt.
TEMP=`getopt -o c:u: --long core:,url: -n "$0" -- "$@"`
#TEMP=`getopt -o c:lu:w: --long core:,local,url:,working_dir: -n "$0" -- "$@"`

if [ $? != 0 ] ; then
  echo "Terminating..." 1>&2 ;
  usage ;
  exit 1 ; 
fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"


core=
cwd=`pwd`
local=
url=
# workingDir=

while true; do
  case "$1" in
    -c | --core )                 core="$2";                                       shift 2 ;;
    -l | --local )                local=1;                                         shift;;
    -u | --url )                  url="$2";                                        shift 2 ;;
#    -w | --working_dir )          workingDir="$2";                                 shift 2 ;;
         -- )                                                                      shift;      break ;;
    * )                           echo "Unknown option '$1' found !" ; usage ;                 break ;;
  esac
done


# if [ -z "$workingDir" ]; then
#   usage
# fi


echo ""
echo "core        : $core"
echo "cwd         : $cwd"
echo "url         : $url"
# echo "working_dir : $workingDir"
echo ""


# git config --global --add safe.directory /myLocalWorkingDir
# git config --global --add safe.directory $workingDir
# returnValue=$?


apt-get install -y python3-semver

returnValue=0

if [ "$core" = "local" ]; then
    python3 extras/arduino-devops/arduino-packager.py --no-previous-releases
    returnValue=$(($returnValue | $?))
    python3 extras/arduino-devops/pckg-install-local.py --pckg-dir build
    returnValue=$(($returnValue | $?))
else
    arduino-cli core install --config-file /root/.arduino15/arduino-cli.yaml $core --additional-urls $url
    returnValue=$(($returnValue | $?))
fi


echo "returnValue : $returnValue"
echo "$0 done."
exit $returnValue
