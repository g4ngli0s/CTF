## **Enunciado**

Mayday Mayday  
Points: 150 
Country: South Africa   
Attatchment: https://mega.nz/#!HpYxUIIZ!TjDhMDCvazuay1Cats4zObHuRmixGhVa7Sy0-5hnLTg    
Description: Hi aspirant, we lost all our carrots, for this reason we need your skills so please... try to steal the private bank of carrots for us. The time begins...NOW!

## **Solución**

La verdad es que no sé para que he publicado este writeup porque es el clásico ejemplo de crackme sencillo y sin mucha sustancia. Pero luego un amigo me ha convencido para ponerlo aunque sea sólo para configurar las opciones del gdb-peda :-)
Para quien no lo sepa, 'peda' es un script de python que te ayuda a no "quemarte tanto las pestañas" en gdb. Te aporta un entorno visual más amigable y funcionalidades extra no incluídas en gdb. Para quien quiera conocer más:
https://github.com/longld/peda
De todas formas yo suelo usar 'voltron', que a diferencia de peda te permite redirigir la salida a otros terminales:
https://github.com/snare/voltron


Estas son las opciones que suelo usar en .gdbinit:

```
set history save
set confirm off
set verbose off
set print pretty on
set print array off
set print array-indexes on
set python print-stack full
set disassembly-flavor intel
source ~/peda/peda.py
```

Comencemos por lo básico respecto al binario:

```
file fwhibbit-150 
fwhibbit-150: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=bd3ef4bb0664dc621aefcbda1f311aee8a832a9e, not stripped
```

Tenemos un binario que al ejecutarse nos pide una contraseña... Sí, es lo que estáis pensando, lo único que vamos a hacer es poner un breakpoint después de introducir nuestro chorizo correspondiente de AAAA's y ver con que cadena compara la nuestra. Así de sencillo, tendremos la contraseña con tan sólo pasar de hexadecimal a ascii el contenido de memoria.

Lo primero es poner el breakpoint después de introducir nuestra contraseña, para ello buscaremos alguna función tipo scanf:

```
   0x00000000004008eb <+510>:	lea    rax,[rbp-0x90]
   0x00000000004008f2 <+517>:	mov    rsi,rax
   0x00000000004008f5 <+520>:	mov    edi,0x400e9d
   0x00000000004008fa <+525>:	mov    eax,0x0
=> 0x00000000004008ff <+530>:	call   0x4005f0 <__isoc99_scanf@plt>
   0x0000000000400904 <+535>:	lea    rdx,[rbp-0x90]
   0x000000000040090b <+542>:	lea    rax,[rbp-0xe0]
   0x0000000000400912 <+549>:	mov    rsi,rdx
   0x0000000000400915 <+552>:	mov    rdi,rax
=> 0x0000000000400918 <+555>:	call   0x4005d0 <strcmp@plt>
   0x000000000040091d <+560>:	test   eax,eax
```

Bueno, viendo el ensamblador nos saltamos ese breakpoint vamos directamente a lo que nos interesa, la función strcmp:

```
br *0x0000000000400918
```

La función strcmp recibe como parámetros el origen (registro $rsi) y el destino (registro $rdi), por lo tanto con mirar esas posciones de memoria tendremos por un lado nuestra entrada en la posición que apunta $rsi y por otro lado la contraseña que está en la posición que apunta $rdi:

```
x/32xw $rsi
0x7fffffffe0f0:	0x41414141	0x00000000	0xf7de7a44	0x00007fff

x/32xw $rdi
0x7fffffffe0a0:	0x6c6c756e	0x00000000	0xffffe001	0x00007fff
```

Pasando '0x6c6c756e' a ascii: 'llun' ya tenemos la contraseña. Ahora ejecutamos y nos da la flag:

```
./fwhibbit-150 
||====================================================================||
||//$//////////////////////////////////////////////////////////////$//||
||(100)================| RESERVE BANK OF FWHIBBIT |==============(100)||
||//$//        ~         '------========--------'                //$//||
||<< /        /$/              // ____ //                         / >>||
||>>|        //L//            // ///..) //              XXXX       |<<||
||<<|        // //           || <||  >}  ||                        |>>||
||>>|         /$/            ||  $$ --/  ||          XXXXXXXXX     |<<||
||<<|     Free to Use        *||  ||_/  //*                        |>>||
||>>|                         *||/___|_//*                         |<<||
||<</      Rating: E     _____/ FWHIBBIT /________    XX XXXXX     />>||
||//$/                 ~|  REPUBLIC OF FWHIBBIT   |~              /$//||
||(100)===================  ONE HUNDRED CARROTS =================(100)||
||//$//////////////////////////////////////////////////////////////$//||
||====================================================================||
Fwhibbit Control Access
Enter our password:
null
You Win
fwhibbit{fwhibbit_reversing_rul3s}
```

Un reto ideal para lammers como nosotros :-)


