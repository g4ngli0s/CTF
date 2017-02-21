## **Enunciado**

Red Pill  
Points: 150   
Country: India   
Attatchment: https://mega.nz/#!NlMlkB6I!ypUjeh2I27f9U5cTu1r_XJBROOV-BQJriRvXeKn_xuk     
Description: Deciding between the blue pill or the red pill is a tricky decision. But now...we already make a choice. Try to give the red pill to the rabbits.  



## **Solución**

Este en realidad se supone que era un exploiting pero se podía solucionar haciendo reversing. Veamos las características del binario:

```
file redpill 
redpill: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e3c09eea4928ac041095632410c29d84b538830f, stripped
```
```
gdb-peda$ checksec 
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : Partial
```

Si lo ejecutamos y le pasamos como argumento una cadena de caracteres muy larga va a petar:

```
./redpill AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
 Take the Red Pill!! 

     Red Pill  0x50444552
     Your Pill 0x41414141

  Blue Pill
Segmentation fault

```
Vamos a crear un patrón de caracteres para averiguar el offset con metasploit:

```
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 150
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9
```

Lo metemos en gdb y nos da una dirección que se corresponde con una parte del patrón anteior. Esta dirección se la pasamos a metasploit otra vez y nos da el offset:

```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 150 -q 0x80001660
[*] No exact matches, looking for likely candidates...
```

Ooops, parece que no hay ningún offset. Tendremos que probar a ejecutarlo en gdb y calcular a mano el offset o tener en cuenta la información que nos da al ejecutarlo sobre las posiciones de memoria de Red Pill y Your Pill.    
Lo primero que observamos en el código ensamblador es la necesidad de pasarle un parámetro al ejecutable:

```
    1486:	83 3f 01             	cmp    DWORD PTR [edi],0x1        <== Si sólo hay un parámetro no salta y se para
    1489:	75 3c                	jne    14c7 <main@@Base+0x99>  
```

```
   0x800014de <main+176>:	mov    ebx,esi
=> 0x800014e0 <main+178>:	call   0x80000e20 <strcpy@plt>          <== Función vulnerable que sobreescribe la posición de retorno del stack frame actual
   0x800014e5 <main+183>:	add    esp,0x10
```

La pila antes de llamar a strcpy:

```
0xbffff280:	0xbffff2a5	0xbffff550	0xbffff2e8	0x80001454
0xbffff290:	0xb7eb9740	0x80004085	0x8000407c	0x8000166d
0xbffff2a0:	0xffffffff	0x80004000	0xbffff2c8	0x800016d9
0xbffff2b0:	0x00000001	0x0000ffff	0xb7fa5f2c	0x800016c5
0xbffff2c0:	0xb7dbf3dc	0x80004000	0x00000002	0x0b103743
```

La pila después de llamar a strcpy:

```
0xbffff290:	0xb7eb9740	0x80004085	0x8000407c	0x8000166d
0xbffff2a0:	0xffffffff	0x41414100	0x41414141	0x41414141
0xbffff2b0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff2c0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff2d0:	0x41414141	0x41414141	0xbf004141	0x00000000
```
Si seguimos ejecutando el código, vemos que hay una comparación de una variable local con un valor, que casualmente es el valor de red pill:
```
   0x80001510 <main+226>:	add    esp,0x10
=> 0x80001513 <main+229>:	cmp    DWORD PTR [ebp-0x1c],0x50444552     <== Valor de red pill
   0x8000151a <main+236>:	jne    0x8000161a <main+492>
```

Este valor de redpill lo hemos sobrescrito cuando hemos llamado a la función strcpy como se puede ver en la memoria:

```
x/32xw $ebp-0x1c
0xbffff27c:	0x41414141	0x41414141	0x41414141	0x41414141
```

Si en el gdb directamente cambiamos ese valor:

```
set {int}0xbffff27c=0x50444552
```

Vemos que ahora el contenido de la posición de memoria va a coincidir con el valor de red pill:

```
x/32xw $ebp-0x1c
0xbffff27c:	0x50444552	0x41414141	0x41414141	0x41414141
```

Si seguimos ejecutando el programa dentro de gdb:

```
gdb-peda$ c
Continuing.

  Red Pill
  fwhibbit{t4ke-b0th_1346651474} 

Program received signal SIGSEGV, Segmentation fault.
```

¡Bingo! Ya tenemos el flag y sin tener que escribir ningún cutre script de explotación :)

