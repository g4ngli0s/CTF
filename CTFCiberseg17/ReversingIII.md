Datos del ejecutable que nos proporcionan:

```
file d1c53e27b0580fdf3e9addffc06359a5 
d1c53e27b0580fdf3e9addffc06359a5: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=53abe7e0d73dd74756eedf50a52b01a5937e1c73, not stripped
```

Si lo ejecutamos vemos que nos pide una clave para solucionarlo:

```
./d1c53e27b0580fdf3e9addffc06359a5 
[USAGE] ./d1c53e27b0580fdf3e9addffc06359a5 <password>
```

Si metemos una contraseña cualquiera:

```
./d1c53e27b0580fdf3e9addffc06359a5 djkfl
Incorrect password!
```

Con strings se pueden ver las cadenas:

```
strings d1c53e27b0580fdf3e9addffc06359a5
Incorrect password!
[USAGE] %s <password>
```

Pero no hay ninguna cadena de password correcta o algo parecido.
Echemos un vistazo a las funciones más significativas del binario:

```
objdump -t d1c53e27b0580fdf3e9addffc06359a5 

d1c53e27b0580fdf3e9addffc06359a5:     file format elf32-i386

SYMBOL TABLE:

00000000 l    df *ABS*	00000000              main.c
00000000 l    df *ABS*	00000000              crtstuff.c
08048527 g     F .text	00000062              two
08048589 g     F .text	00000062              one
080484bb g     F .text	0000006c              main
080485eb g     F .text	00000063              check_pass
0804864e g     F .text	0000001b              usage
```

Parece que check_pass es nuestro candidato ideal ejecutar con el debugger a ver que nos dice.
Desde la función main se hace una llamada a check_pass:

```
0x080484eb <+48>:	mov    eax,DWORD PTR [eax+0x4]
0x080484ee <+51>:	add    eax,0x4
0x080484f1 <+54>:	mov    eax,DWORD PTR [eax]
0x080484f3 <+56>:	sub    esp,0xc
0x080484f6 <+59>:	push   eax
0x080484f7 <+60>:	call   0x80485eb <check_pass>
```

Veamos a analizar que ocurre en check_pass:

```
disas check_pass
Dump of assembler code for function check_pass:
   0x080485eb <+0>:	push   ebp
   0x080485ec <+1>:	mov    ebp,esp
   0x080485ee <+3>:	sub    esp,0x18
   0x080485f1 <+6>:	sub    esp,0xc
   0x080485f4 <+9>:	push   DWORD PTR [ebp+0x8]
   0x080485f7 <+12>:	call   0x8048390 <strlen@plt> 			<--- Calcula la longitud de la password
   0x080485fc <+17>:	add    esp,0x10
   0x080485ff <+20>:	cmp    eax,0x5							<--- La compara con 5
   0x08048602 <+23>:	ja     0x804860b <check_pass+32>		<--- Tiene que ser mayor igual que 5. Si no sale de la función y envía el mensaje "Incorrect password!"
   0x08048604 <+25>:	mov    eax,0x1
   0x08048609 <+30>:	jmp    0x804864c <check_pass+97>
   0x0804860b <+32>:	sub    esp,0xc
   0x0804860e <+35>:	push   DWORD PTR [ebp+0x8]
   0x08048611 <+38>:	call   0x8048390 <strlen@plt>			<--- Comprueba otra vez la longitud de la cadena
   0x08048616 <+43>:	add    esp,0x10
   0x08048619 <+46>:	mov    DWORD PTR [ebp-0x14],eax
   0x0804861c <+49>:	mov    DWORD PTR [ebp-0x10],0x0
   0x08048623 <+56>:	mov    DWORD PTR [ebp-0xc],0x0
   0x0804862a <+63>:	jmp    0x8048641 <check_pass+86>		<--- Entra en un bucle con i=longitud de la cadena
   0x0804862c <+65>:	mov    edx,DWORD PTR [ebp-0xc]			
   0x0804862f <+68>:	mov    eax,DWORD PTR [ebp+0x8]
   0x08048632 <+71>:	add    eax,edx							<--- Lo que hace básicamente es sumar el valor ascii de los caracteres de la cadena y los guarda en eax
   0x08048634 <+73>:	movzx  eax,BYTE PTR [eax]
   0x08048637 <+76>:	movsx  eax,al
   0x0804863a <+79>:	add    DWORD PTR [ebp-0x10],eax
   0x0804863d <+82>:	add    DWORD PTR [ebp-0xc],0x1
   0x08048641 <+86>:	mov    eax,DWORD PTR [ebp-0xc]
   0x08048644 <+89>:	cmp    eax,DWORD PTR [ebp-0x14]			<--- Comprueba la condición de salida del bucle
   0x08048647 <+92>:	jl     0x804862c <check_pass+65>		<--- Sigue en el bucle si es menor que la longitud, si no sale
   0x08048649 <+94>:	mov    eax,DWORD PTR [ebp-0x10]
   0x0804864c <+97>:	leave  
   0x0804864d <+98>:	ret    
End of assembler dump.
```

Lo acabo mañana, era más largo de lo que pensaba :)
