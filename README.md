# throttle-status
Raspberry Pi vcgencmd get_throttled human readable output.<br>
A script to read the throttle status of your rpi. 

```
usage: throttle-status.py [-h] [--hex [HEX]] [--get]

Raspberry Pi throttling status report.

optional arguments:
  -h, --help   show this help message and exit
  --hex [HEX]  Prints a text-based throttling status by hex value.
  --get        Prints the "vcgencmd get_throttled" command's output in human
               readable format.
               
The console output displaying the results in the following format:
```

```
111100000000000001010
||||             ||||_ under-voltage
||||             |||_ currently throttled
||||             ||_ arm frequency capped
||||             |_ soft temperature reached
||||_ under-voltage has occurred since last reboot
|||_ throttling has occurred since last reboot
||_ arm frequency capped has occurred since last reboot
|_ soft temperature reached since last reboot
```