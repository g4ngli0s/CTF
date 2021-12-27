## **Enunciado**

Tobacco Santa  
Description: Dr. Kringle has been recently trying to expand his joy-bringing business to the adult sector, but after seeing his latest startup we're not so sure if he's going in the right direction. Can you help him reconsider?

## **Solución**

Después de unas cuantas horas me di cuenta de que había que aplicar la técnica SROP.


Veamos las características del binario:

```
file ./main     
./main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped
```
```
[+] checksec for '/home/kali/tmp/xmas/main'
Canary                        : ✘ 
NX                            : ✘ 
PIE                           : ✘ 
Fortify                       : ✘ 
RelRO                         : ✘ 
```
