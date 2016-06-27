#######################
#
#  This script is used to define the configuration points of the server router
#
#######################

import os.path
import sys
import binascii

#jvm path marker
cert_off = 200 * 2
cert_name = '\x00\x00\x22\x00\x26\x00\x29\x00\x2c'

#reg key path
reg_off = 200 * 2
reg_str = '\x00\x00\x26\x00\x23\x00\x17\x00\x21'

def encodeStr( word ):
  out = ''
  for i in word:
    o = ord(i)
    #print hex(o)
    nib_l = o & 0x0f
    nib_h = (o & 0xf0) >> 4
    out += chr(nib_h) + chr(nib_l)
  return out
  
def setRegKeyPath( filepath ):
  print "\nEnter the print monitor registry key name"
  sys.stdout.write('> ')
  reg_in = raw_input()
  if len(reg_in) > 200 / 2:
    print "Error: Length of registry name too long. Max Length = 100"
    return
  
  #convert to unicode
  reg_in = encodeStr(reg_in)
  uni_reg = reg_in.encode('utf16')[2:] + "\x00\x00\x00\x00"
  
  #Open the file
  f = open(filepath, 'rb')
  data = f.read()
  f.close()  

  #Find port marker
  idx = data.find(reg_str)
  #print "Index: ", idx
  reg_str_off = idx - reg_off
  #print binascii.hexlify(data[port_str_off: port_str_off + port_off ])
  #print "Current certificate name: " + data[cert_str_off: cert_str_off + cert_off ]
  
  #Overwrite the string
  fh = open(filepath, "r+b")
  fh.seek(reg_str_off)
  fh.write(uni_reg)
  fh.close()
  
def setJvmPath( filepath ):
  print "\nEnter the JVM Path"
  sys.stdout.write('> ')
  cert_in = raw_input()
  if len(cert_in) > 200 / 2:
    print "Error: Length of certificate string too long. Max Length = 100"
    return
  
  #convert to unicode
  cert_in = encodeStr(cert_in)
  uni_port = cert_in.encode('utf16')[2:] + "\x00\x00\x00\x00"
  
  #Open the file
  f = open(filepath, 'rb')
  data = f.read()
  f.close()  

  #Find port marker
  idx = data.find(cert_name)
  #print "Index: ", idx
  cert_str_off = idx - cert_off
  #print binascii.hexlify(data[port_str_off: port_str_off + port_off ])
  #print "Current certificate name: " + data[cert_str_off: cert_str_off + cert_off ]
  
  #Overwrite the string
  fh = open(filepath, "r+b")
  fh.seek(cert_str_off)
  fh.write(uni_port)
  fh.close()
  
def print_menu():
  print "\nConfiguration Menu:"
  print "-------------------"
  print "1. Set JVM library directory (ex. C:\Program Files\Java\jre7\bin\client)"
  print "2. Set Authentication String"
  print "3. Quit\n"
  sys.stdout.write('> ')
  return raw_input()

if len (sys.argv) == 2:  
  (progname, filepath) = sys.argv  
else:  
  print len (sys.argv)  
  print 'Usage: {0} <file path>'.format (sys.argv[0])  
  exit (1) 
  
#Check that the file exists
if os.path.isfile(filepath) == False:
  print '\n[-] Error: "%s" doesnt exist.' % filepath
  exit (1)
  
#Print menu
while(1):
  choice = print_menu() 
  if choice == '1':
    setJvmPath(filepath)
  elif choice == '2':
    setRegKeyPath(filepath) 
  elif choice == '3':
    exit(1)