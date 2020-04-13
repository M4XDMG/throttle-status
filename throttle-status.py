import argparse
import subprocess

hex2bin_map = {
   "0":"0000",
   "1":"0001",
   "2":"0010",
   "3":"0011",
   "4":"0100",
   "5":"0101",
   "6":"0110",
   "7":"0111",
   "8":"1000",
   "9":"1001",
   "A":"1010",
   "B":"1011",
   "C":"1100",
   "D":"1101",
   "E":"1110",
   "F":"1111",
}

err_map = {
   0 : "soft temperature reached since last reboot",
   1 : "arm frequency capped has occurred since last reboot",
   2 : "throttling has occurred since last reboot",
   3 : "soft temperature reached",
   16 : "soft temperature reached",
   17 : "arm frequency capped",
   18 : "currently throttled",
   19 : "under-voltage",
}

queryStatus = ["vcgencmd", "get_throttled"]

def parseHexValue(hexValue):
   result = str()
   for i in hexValue:
       result = result + (hex2bin_map.get(i.upper()))
   return result

def processBinaryStatus(binary):
   print(binary)
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

parser = argparse.ArgumentParser(description="Raspberry Pi throttling status report.")
parser.add_argument("--hex", nargs="?", type=str, help="Prints a text-based throttling status by hex value.")
parser.add_argument("--get", action='store_true', help="Prints the \"vcgencmd get_throttled\" command's output in human readable format.")

args = parser.parse_args()

if args.hex:
    hexa = ''.join(args.hex).strip()
    if hexa[0:2] == "0x" and len(hexa) <= 7:
        processBinaryStatus(parseHexValue(hexa[2:]))
    else:
        print("\nERROR: Could not parse hex value. Make sure you entered the argument in the proper format: 0x*****\n")
        parser.print_help()
elif args.get:
    process = subprocess.run(queryStatus, capture_output=True)
    if (process.returncode == 0):
        response = process.stdout.decode('ascii').strip().split("=")[1][2:]
        processBinaryStatus(parseHexValue(response))
    else:
        print("\nERROR: Could not run command " + str(queryStatus) + ". ")
        print("STDERRR: " + str(process.stderr.decode('ascii')))
        parser.print_help()
