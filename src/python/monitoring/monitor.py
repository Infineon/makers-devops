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

    Methods
    -------
        read_unity_serial(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = "Unity test run", end_token = "^OK|^FAIL",
                          error_token = "ERROR ", warn_token = "WARN ", report_file = "unity.log"):
            Low-level method to parse Unity unit test output read from the serial device.

        parseUnityOutput(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = "Unity test run", end_token = "^OK|^FAIL",
                         error_token = "ERROR ", warn_token = "WARN ", report_file = "unity.log")
            High-level method to parse Unity unit test output read from the serial device.

        read_example_serial(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = ".*", end_token = ".*",
                            error_token = "ERROR|FATAL", warn_token = "WARNING|WARN", report_file = "example.log")
            Low-level method to parse example test output read from the serial device.

        parseExampleOutput(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = ".*", end_token = ".*",
                           error_token = "ERROR|FATAL", warn_token = "WARNING", report_file = "example.log")
            High-level method to parse example test output read from the serial device.
    """


    # def read_unity_serial(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = "^TEST\(", end_token = "^OK|^FAIL",
    def read_unity_serial(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = "Unity test run", end_token = "^OK|^FAIL",
                          error_token = "ERROR ", warn_token = "WARN ", report_file = "unity.log"):
        """
        Function reading from the serial port for the time specified by 'runtime'. It starts analyzing the output
        between 'start_token' and 'end_token'.

            Parameters:
            -----------
                serial_object (obj) : The serial object related to the device's comport.
                baudrate (int)      : The baud speed rate for this serial port.
                runtime (int)       : The maximum time to collect data from the port.
                start_token (str)     : Begin token to start parsing output.
                end_token (str)       : End token to stop parsing data.
                error_token (str)     : The token for an error message.
                warn_token (str)      : The token for a warning message.
                report_file (str)   : Name of output log file.

            Returns:
            --------
                errors (list)             : List of error messages.
                warnings (list)           : List of warning messages.
                summary (list)            : Summary list, i.e. total number of tests, number of failed as well as ignored tests.
                start token found (boolean) : Wether the start token has been found.
                end token found (boolean)   : Wether the end token has been found.
        """
        error_pattern   = re.compile(error_token, re.IGNORECASE)
        warn_pattern    = re.compile(warn_token, re.IGNORECASE)
        summary_pattern = re.compile(r'.*Tests.*Failures.*Ignored', re.IGNORECASE)
        number_pattern  = re.compile(r'[\d]+')

        start_time  = time.time()
        end_time    = start_time + runtime
        start_found = False
        end_found   = False
        errors      = []
        warnings    = []
        summary     = []
        print(f"monitor  start_time : {start_time}   end_time : {end_time}")
        try:
            with open(report_file, 'w') as filehandle:
                while (time.time() < end_time) and not (start_found and end_found):
                    print(f"Monitor looping {time.time()} ?<=?  {end_time}")
                    sys.stdout.flush()
                    try:
                        # line = serial_object.readline().decode().strip()
                        line = serial_object.readline()
                        print(f"1 line : {line}")
                        sys.stdout.flush()

                        line = line.decode()
                        print(f"2 line : {line}")
                        sys.stdout.flush()

                        line = line.strip()
                        print(f"3 line : {line}")
                        sys.stdout.flush()
                    except ValueError as ve:
                        print(line)
                        print(f"FATAL: ValueError Could not read from serial !")
                        sys.stdout.flush()
                        return errors, warnings, summary, start_found, end_found
                    except SerialException as se:
                        print(line)
                        print(f"FATAL: SerialException Could not read from serial !")
                        sys.stdout.flush()
                        return errors, warnings, summary, start_found, end_found
                    except:
                        print(line)
                        print(f"FATAL: Some other exception  Could not read from serial !   {sys.exc_info()[0]}")
                        sys.stdout.flush()
                        return errors, warnings, summary, start_found, end_found
                    
                    
                    if re.search(start_token, line, re.IGNORECASE) and not end_found:
                        start_found = True

                    if re.search(end_token, line, re.IGNORECASE) and start_found:
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

        except FileNotFoundError:
            print(line)
            print(f"FATAL: FileNotFoundError Could not open file '{report_file}' !")
            sys.stdout.flush()
        except PermissionError:
            print(line)
            print(f"FATAL: PermissionError Could not open file '{report_file}' !")
            sys.stdout.flush()
        except OSError:
            print(line)
            print(f"FATAL: OSError  Could not open file '{report_file}' !")
            sys.stdout.flush()
        except:
            print(line)
            print(f"FATAL: Some other exception  Could not open file '{report_file}' !  {sys.exc_info()[0]}")
            sys.stdout.flush()

        
        return errors, warnings, summary, start_found, end_found


    # def parseUnityOutput(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = "^TEST\(", end_token = "^OK|^FAIL",
    def parseUnityOutput(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = "Unity test run", end_token = "^OK|^FAIL",
                         error_token = "ERROR ", warn_token = "WARN ", report_file = "unity.log"):
        """
        Function collects data from the serial port either for the period of the runtime or
        if for all between begin and end tokens

            Parameters:
            -----------
                serial_object (obj) : The serial object related to the device's comport.
                baudrate (int)      : The baud speed rate for this serial port.
                runtime (int)       : The maximum time to collect data from the port.
                start_token (str)     : Begin token to start parsing output.
                end_token (str)       : End token to stop parsing data.
                error_token (str)     : The token for an error message.
                warn_token (str)      : The token for a warning message.
                report_file (str)   : Name of output log file.

            Returns:
            --------
                errors (list)             : List of error messages.
                warnings (list)           : List of warning messages.
                summary (list)            : Summary list, i.e. total number of tests, number of failed as well as ignored tests.
                start token found (boolean) : Whether the start token has been found.
                end token found (boolean)   : Whether the end token has been found.
        """
        print(f"""Monitor params : start_token : {start_token}   end_token : {end_token} """)
        error_list, warn_list, summary, start_found, end_found = self.read_unity_serial(serial_object, baudrate, runtime, start_token, end_token, error_token, warn_token, report_file)

        if start_found and end_found:
            if len(summary) == 3:
                print("\n\nError List\n##########")

                for line in error_list:
                    print(line)


                print("\n\nWarning List\n############")

                for line in warn_list:
                    print(line)


                print("\n\nSummary\n#######")
                print("Number of tests         : ", summary[0])
                print("Number of failed tests  : ", summary[1])
                print("Number of ignored tests : ", summary[2])
            else:
                print(f"\nFailed to find summary in output. Make sure to have set the correct port and baudrate.\n")

        else:
            print(f'\nFailed to read Unity output ! {"Start" if not start_found else "End"} token not found !\nMake sure to have set the correct port and baudrate.\n')


        return( 1 if (len(summary) == 3 and int(summary[1]) > 0) or (len(summary) != 3) or (int(summary[0]) == 0) or not start_found or not end_found else 0 )



    def read_example_serial(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = ".*", end_token = ".*",
                            error_token = "ERROR|FATAL", warn_token = "WARNING|WARN", report_file = "example.log"):
        """
        Function reading from the serial port for the time specified by 'runtime'. It starts analyzing the output between 'start_token' and 'end_token'.

            Parameters:
            -----------
                serial_object (obj) : The serial object related to the device's comport.
                baudrate (int)      : The baud speed rate for this serial port.
                runtime (int)       : The maximum time to collect data from the port.
                start_token (str)     : Begin token to start parsing output.
                end_token (str)       : End token to stop parsing data.
                error_token (str)     : The token for an error message.
                warn_token (str)      : The token for a warning message.
                report_file (str)   : Name of output log file.

            Returns:
            --------
                errors (list)             : List of error messages.
                warnings (list)           : List of warning messages.
                summary (list)            : Summary list, i.e. total number of errors and warnings.
                start token found (boolean) : Whether the start token has been found.
                end token found (boolean)   : Whether the end token has been found.
        """
        error_pattern   = re.compile(error_token, re.IGNORECASE)
        warn_pattern    = re.compile(warn_token, re.IGNORECASE)

        start_time  = time.time()
        end_time    = start_time + runtime
        start_found = False
        end_found   = False
        errors      = []
        warnings    = []
        summary     = []
        
        try:
            with open(report_file, 'w') as filehandle:
                while (time.time() < end_time) and not (start_found and end_found):
                    try:
                        line = serial_object.readline().decode().strip()
                        # print(line, flush = True)
                    except:
                        return errors, warnings, summary, start_found, end_found
                    
                    if re.search(start_token, line, re.IGNORECASE) and not end_found:
                        start_found = True

                    if re.search(end_token, line, re.IGNORECASE) and start_found:
                        end_found = True

                    if start_found:
                        print(line, flush = True, file = filehandle)
                        print(line, flush = True)

                        if error_pattern.search(line):
                            errors.append(line)

                        if warn_pattern.search(line):
                            warnings.append(line)

        except:
            pass

        summary = [ len(errors), len(warnings) ]
        return errors, warnings, summary, start_found, end_found


    def parseExampleOutput(self, serial_object = None, baudrate = 115200, runtime = 30, start_token = ".*", end_token = ".*",
                           error_token = "ERROR|FATAL", warn_token = "WARNING", report_file = "example.log"):
        """
        Function collects data from the serial port either for the period of the runtime or
        if for all between begin and end tokens

            Parameters:
            -----------
                serial_object (obj) : The serial object related to the device's comport.
                baudrate (int)      : The baud speed rate for this serial port.
                runtime (int)       : The maximum time to collect data from the port.
                start_token (str)     : Begin token to start parsing output.
                end_token (str)       : End token to stop parsing data.
                error_token (str)     : The token for an error message.
                warn_token (str)      : The token for a warning message.
                report_file (str)   : Name of output log file.

            Returns:
            --------
                errors (list)             : List of error messages.
                warnings (list)           : List of warning messages.
                summary (list)            : Summary list, i.e. total number of tests, number of failed as well as ignored tests.
                # start token found (boolean) : Wether the start token has been found.
                # end token found (boolean)   : Wether the end token has been found.
        """
        error_list, warn_list, summary, start_found, end_found = self.read_example_serial(serial_object, baudrate, runtime, start_token, end_token, error_token, warn_token, report_file)

        if start_found and end_found:
            if len(summary) == 2:
                print("\n\nError List\n##########")

                for line in error_list:
                    print(line)


                print("\n\nWarning List\n############")

                for line in warn_list:
                    print(line)


                print("\n\nSummary\n#######")
                print("Number of errors   : ", summary[0])
                print("Number of warnings : ", summary[1])
            else:
                print(f"\nFailed to find summary in output. Make sure to have set the correct port and baudrate.\n")

        else:
            print(f'\nFailed to read example output ! {"Start" if not start_found else "End"} token not found !\nMake sure to have set the correct port and baudrate.\n')


        # return( 1 if (len(summary) == 2 and int(summary[1]) > 0) or (len(summary) != 2) else 0 )
        return( 1 if (len(summary) == 2 and int(summary[1]) > 0) or (len(summary) != 2) or not start_found or not end_found else 0 )
