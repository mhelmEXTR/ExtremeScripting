######################################################################################
#                                                                                    #
# Usage: load script macoui [vr-Mgmt|vr-Default]                                     #
#                                                                                    #
# The VR specified is the VR through which http://macvendors.co/api can be reached.  #
#                                                                                    #
# It is assumed that a dns name-server has been configured on the appropriate VR     #
#                                                                                    #
######################################################################################

import requests, re, ast, exsh, os, sys

def printline(mac, vlan, port):
   try:
      req = 'http://macvendors.co/api/{}'.format(mac)
      r = requests.get(req, timeout=5)
      man = ast.literal_eval(r.text)
      try:
         man = man['result']['company']
      except:
         man = 'Unknown'
      print('Manuf: {} - MAC: {} - Port: {} - VLAN: {}'.format(man, mac, port, vlan))
   except:
      pass
   return('None')

if __name__ == '__main__':
   if (len(sys.argv) != 2):
      print('Usage: load script macoui [vr-Mgmt|vr-Default]')
      raise SystemExit
   else:
      if (re.search('vr-Mgmt',sys.argv[1],re.IGNORECASE) or re.search('vr-Default',sys.argv[1],re.IGNORECASE)):
         if (re.search('vr-Mgmt',sys.argv[1])):
            os.environ['EXOS_VR_ID'] = '0'
         else:
            os.environ['EXOS_VR_ID'] = '2'
         exsh.clicmd('disable cli prompt')
         shfdb = exsh.clicmd('show fdb', True)
         for line in shfdb.splitlines():
            if re.match('..:..:..:..:..:..', line):
               mac = line.split()[0]
               vlan = line.split()[1]
               port = line.split()[-1]
               printline(mac, vlan, port)