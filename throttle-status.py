import sys
import argparse
import subprocess

print("Running with Python version: " + sys.version)

hex2bin_map = {
   "0": "0000",
   "1": "0001",
   "2": "0010",
   "3": "0011",
   "4": "0100",
   "5": "0101",
   "6": "0110",
   "7": "0111",
   "8": "1000",
   "9": "1001",
   "A": "1010",
   "B": "1011",
   "C": "1100",
   "D": "1101",
   "E": "1110",
   "F": "1111",
}

err_map = {
   0: "soft temperature reached since last reboot",
   1: "arm frequency capped has occurred since last reboot",
   2: "throttling has occurred since last reboot",
   3: "under-voltage has occurred since last reboot",
   16: "soft temperature reached",
   17: "arm frequency capped",
   18: "currently throttled",
   19: "under-voltage",
}

queryStatus = ["vcgencmd", "get_throttled"]


def parseHexValue(hexValue):
   result = str()
   for i in hexValue:
       result = result + (hex2bin_map.get(i.upper()))
   return result


def processBinaryStatus(binary):
   print("\n" + binary)
   rows = 0

   errs = {}
   for i in range(len(binary)):
      if binary[i] == "1":
         errs[i] = err_map.get(i)
         rows += 1

   for i in range(rows):
      result = ""
      for j in range(len(binary)):
         if binary[j] == "1":
            if j == max(errs.keys()):
               result = result + "|_" + str(errs.get(j))
               break
            else:
               result = result + "|"
         else:
            result = result + " "
      errs.pop(max(errs.keys()))
      print(result)
   print("\n")


def returnProcessError(queryStatus, stdErr):
    print("\nERROR: Could not run command '" + str(queryStatus) + "'")
    print("STDERRR: " + str(stdErr))


parser = argparse.ArgumentParser(description="Raspberry Pi throttling status report.")
parser.add_argument("--hex", nargs="?", type=str, help="Prints a text-based throttling status by hex value.")
parser.add_argument("--get", action='store_true', help="Prints the \"vcgencmd get_throttled\" command's output in human readable format.")

args = parser.parse_args()

if args.hex:
    hexa = ''.join(args.hex).strip()
    if hexa[0:2] == "0x" and len(hexa) <= 7:
        processBinaryStatus(parseHexValue(hexa[2:]))
    else:
        print("\nERROR: Could not parse hex value. Make sure you entered a correct argument!")
        print("Format: 0x***** , Max length: 7 \n")
        parser.print_help()

elif args.get:
    if sys.version_info[0] == 2 and sys.version_info[1] >= 7:
        process = subprocess.Popen(queryStatus, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
        stdOut = process.stdout.read()
        stdErr = process.stderr.read()
        rc = process.returncode

        if rc == 0:
            response = stdOut.strip().split("=")[1][2:]
            processBinaryStatus(parseHexValue(response))
        else:
            returnProcessError(' '.join(queryStatus), stdErr)
            parser.print_help()

    elif sys.version_info[0] == 3 and sys.version_info[1] >= 5:
        process = subprocess.run(queryStatus, capture_output=True)

        if process.returncode == 0:
            response = process.stdout.decode('ascii').strip().split("=")[1][2:]
            processBinaryStatus(parseHexValue(response))
        else:
            returnProcessError(' '.join(queryStatus), process.stderr.decode('ascii'))
            parser.print_help()

    else:
        print("\nERROR: Your Python version (" + sys.version + ") is below the minimum supported version (2.4)!")
        sys.exit()
