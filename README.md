# Website IP Tracker

## Description
Website IP Tracker is a simple Python script that allows you to find the IP address of any website. The script can handle single domains or multiple domains listed in a file. Results can be saved to a text file for future reference.

## Features
- Track the IP address of a single domain.
- Track the IP addresses of multiple domains from a file.
- Save the results to a text file.
- Display the current version of the script.

## Usage
To display the help message:
```sh
python3 tracker.py
```
##To track the IP address of a single domain:
```sh
python3 tracker.py -d example.com
```

## To track the IP addresses of multiple domains listed in a file:
```sh
python3 tracker.py -f domains.txt
```

## To save the results to a text file:
```sh
python3 tracker.py -d example.com -s
```

## Example Output
```sh
example.com | 93.184.216.34
```

## Banner
```sh
         
         ██████╗░░█████╗░██╗░░░░░██████╗░░██╗░░░░░░░██╗██╗███╗░░██╗
         ██╔══██╗██╔══██╗██║░░░░░██╔══██╗░██║░░██╗░░██║██║████╗░██║
         ██████╦╝███████║██║░░░░░██║░░██║░╚██╗████╗██╔╝██║██╔██╗██║
         ██╔══██╗██╔══██║██║░░░░░██║░░██║░░████╔═████║░██║██║╚████║
         ██████╦╝██║░░██║███████╗██████╔╝░░╚██╔╝░╚██╔╝░██║██║░╚███║
         ╚═════╝░╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚══╝

```

## Requirements
- Python 3.x
- requests module

## Note
The project does not have any malicious intent, it is coded for educational purposes only :)
