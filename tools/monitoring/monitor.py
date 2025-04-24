from __future__ import absolute_import

import argparse
import os
import re
import serial
import subprocess
import sys
import time
import yaml

# from enum import IntEnum
from serial.tools.list_ports import comports
from serial.tools import list_ports_linux


importPath = os.path.normpath(
    os.path.dirname(os.path.realpath(os.path.abspath(__file__))) + "/.."
)

if not importPath in sys.path:
    sys.path.insert(1, importPath)


class Monitor:
    """
    A class to monitor hardware ouput to the serial interface.

    ...

    Attributes
    ----------
        aa (dict)
            bb.

    Methods
    -------
        info(additional=""):
            Prints useful HIL status information.
        
        read_device_serial(self, sn):
            Method to switch off and on all devices.
 
    """


    def read_device_serial(self, sn = "", baudrate = 115200, runtime = 30, start_tag = "Unity test run", end_tag = "^OK|^FAIL",
                           error_tag = "ERROR ", warn_tag = "WARN ", report_file = "unity.log"):
        """
        Method to.

            Parameters:
            -----------
                sn (str) : A string representing the device's serial number.

            Returns:
            --------
                output (str) : Output read from device.
        """
        self.parseUnityOutput(self.snToPort[sn])


    def read_serial(self, comport = "", baudrate = 115200, runtime = 30, start_tag = "Unity test run", end_tag = "^OK|^FAIL",
                    error_tag = "ERROR ", warn_tag = "WARN ", report_file = "unity.log"):
        """
        Function reading from the serial port for the time specified by 'runtime'. It starts analyzing the output
        between 'start_tag' and 'end_tag'.

            Parameters:
            -----------
                comport (str)     : A string representing the device's comport.
                baudrate (int)    : The baud speed rate for this serial port.
                runtime (int)     : The maximum time to collect data from the port.
                start_tag (str)   : Begin tag to start parsing output.
                end_tag (str)     : End tag to stop parsing data.
                error_tag (str)   : The tag for an error message.
                warn_tag (str)    : The tag for a warning message.
                report_file (str) : Name of output log file.

            Returns:
            --------
                errors (list)             : List of error messages.
                warnings (list)           : List of warning messages.
                summary (list)            : Summary list, i.e. total number of tests, number of failed as well as ignored tests.
                start tag found (boolean) : Wether the start tag has been found.
                end tag found (boolean)   : Wether the end tag has been found.
        """
        error_pattern   = re.compile(error_tag, re.IGNORECASE)
        warn_pattern    = re.compile(warn_tag, re.IGNORECASE)
        summary_pattern = re.compile(r'.*Tests.*Failures.*Ignored', re.IGNORECASE)
        number_pattern  = re.compile(r'[\d]+')

        start_time  = time.time()
        end_time    = start_time + runtime
        start_found = False
        end_found   = False
        errors      = []
        warnings    = []
        summary     = []
        
        try:
            with serial.Serial(comport, baudrate, timeout=runtime) as ser:
                with open(report_file, 'w') as filehandle:
                    while (time.time() < end_time) and not (start_found and end_found):
                        try:
                            line = ser.readline().decode().strip()
                            print(line)
                        except:
                            return errors, warnings, summary, start_found, end_found
                        
                        if re.search(start_tag, line, re.IGNORECASE) and not end_found:
                            start_found = True

                        if re.search(end_tag, line, re.IGNORECASE) and start_found:
                            end_found = True

                        if start_found:
                            print(line, flush = True, file = filehandle)
                            print(line, flush = True)

                            if error_pattern.search(line):
                                errors.append(line)

                            if warn_pattern.search(line):
                                warnings.append(line)

                            if summary_pattern.search(line):
                                summary = number_pattern.findall(line)

        except:
            pass

        
        return errors, warnings, summary, start_found, end_found


    def parseUnityOutput(self, comport = "", baudrate = 115200, runtime = 30, start_tag = "Unity test run", end_tag = "^OK|^FAIL",
                         error_tag = "ERROR ", warn_tag = "WARN ", report_file = "unity.log"):
        """
        Function collects data from the serial port either for the period of the runtime or
        if for all between begin and end tags

            Parameters:
            -----------
                comport (str)     : A string representing the device's comport.
                baudrate (int)    : The baud speed rate for this serial port.
                runtime (int)     : The maximum time to collect data from the port.
                start_tag (str)   : Begin tag to start parsing output.
                end_tag (str)     : End tag to stop parsing data.
                error_tag (str)   : The tag for an error message.
                warn_tag (str)    : The tag for a warning message.
                report_file (str) : Name of output log file.

            Returns:
            --------
                errors (list)             : List of error messages.
                warnings (list)           : List of warning messages.
                summary (list)            : Summary list, i.e. total number of tests, number of failed as well as ignored tests.
                start tag found (boolean) : Wether the start tag has been found.
                end tag found (boolean)   : Wether the end tag has been found.
        """
        error_array, warn_array, summary, start_found, end_found = self.read_serial(comport, baudrate, runtime, start_tag, end_tag, error_tag, warn_tag, report_file)

        if start_found and end_found:
            if len(summary) == 3:
                print("\n\nError List\n##########")

                for line in error_array:
                    print(line)


                print("\n\nWarning List\n############")

                for line in warn_array:
                    print(line)


                print("\n\nSummary\n#######")
                print("Number of tests         : ", summary[0])
                print("Number of failed tests  : ", summary[1])
                print("Number of ignored tests : ", summary[2])
            else:
                print(f"\nFailed to find summary in output. Make sure to have set the correct port and baudrate.\n")

        else:
            print(f'\nFailed to read Unity output ! {"Start" if not start_found else "End"} tag not found !\nMake sure to have set the correct port and baudrate.\n')


        return( 1 if (len(summary) == 3 and int(summary[1]) > 0) or (len(summary) == 0) or not start_found or not end_found else 0 )
