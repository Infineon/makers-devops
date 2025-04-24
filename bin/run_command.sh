#!/bin/bash


echo "executing $0 $* ..."


usage() {
  echo "Usage: $0 :" 1>&2;
  echo "          [-c | --command] <Command to execute in container, none for interactive mode.>   [-w | --working_dir] <Working directory to execute the command in.>" 1>&2;
  exit 1;
}


# This requires GNU getopt.
TEMP=`getopt -o c:w: --long command:,working_dir: -n "$0" -- "$@"`

if [ $? != 0 ] ; then
  echo "Terminating..." >&2 ;
  usage ;
  exit 1 ; 
fi

# Note the quotes around `$TEMP': they are essential!
eval set -- "$TEMP"


command=
workingDir=

while true; do
  case "$1" in
    -c | --command )              command="$2";                                     shift 2 ;;
    -w | --working_dir )          workingDir="$2";                                  shift 2 ;;
         -- )                                                                       shift;      break ;;
    * )                           echo "Unknown option '$1' found !" ; usage ;                  break ;;
  esac
done


if [ -z "$command" ]; then
  command=$*
elif [ ! -z "$*" ]; then
  usage
fi


if [ -z "$workingDir" ]; then
  workingDir="."
fi


echo ""
echo "command     : $command"
echo "working_dir : $workingDir"
echo ""

cd $workingDir

# run-build-target:
# 	(cd extras/arduino-xensiv-3d-magnetic-sensor-tlx493d ; make -f Makefile.arduino.mk FQBN=$(FQBN) PORT=$(PORT) UNITY_PATH=../arduino-core-tests/Unity $(TARGET))
# 	# (cd extras/arduino-core-tests ; make FQBN=$(FQBN) UNITY_PATH=Unity $(TARGET))
$command
returnValue=$?

echo "$0 done."
exit $returnValue
