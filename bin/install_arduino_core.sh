#!/bin/bash


echo "executing $0 $* ..."


usage() {
  echo "Usage: $0 :" 1>&2;
  echo "          [-c | --core] <Core to be installed.>   [-u | --url] <Url to download core.>" 1>&2;
  exit 1;
}


# This requires GNU getopt.
TEMP=`getopt -o c:u: --long core:,url: -n "$0" -- "$@"`

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
    -u | --url )                  url="$2";                                        shift 2 ;;
         -- )                                                                      shift;      break ;;
    * )                           echo "Unknown option '$1' found !" ; usage ;                 break ;;
  esac
done


echo ""
echo "core        : $core"
echo "cwd         : $cwd"
echo "url         : $url"
echo ""


returnValue=0

if [ "$core" = "local" ]; then
    if [ -d "build" ]; then
        rm -rf build
    fi

    bash tools/dev-setup.sh

    python3 extras/arduino-devops/arduino-packager.py --no-previous-releases
    returnValue=$(($returnValue | $?))

    python3 extras/arduino-devops/pckg-install-local.py --pckg-dir build
    returnValue=$(($returnValue | $?))

    chown -R --reference=. build
    chown -R --reference=. cores

else
    arduino-cli core install $core --additional-urls $url
    returnValue=$(($returnValue | $?))
fi


udevDir=`find ~/.arduino15/packages/infineon/tools/openocd -name udev_rules`
/opt/makers-hil/bin/install_psoc6_udev.sh ${udevDir}

/opt/makers-hil/bin/install_segger_udev.sh /opt/SEGGER/JLink/

arduino-cli core update-index
arduino-cli board list


echo "returnValue : $returnValue"
echo "$0 done."
exit $returnValue
