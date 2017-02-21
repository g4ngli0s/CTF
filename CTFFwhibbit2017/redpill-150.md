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

Ooops, parece que no hay ningún offset. Tendremos que probar a ejecutarlo en gdb y calcular a mano el offset o tener en cuenta la información que nos da al ejecutarlo sobre las posiciones de memoria de Red Pill y Your Pill. Veamos el código ensamblador:


