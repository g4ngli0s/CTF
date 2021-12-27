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
checksec --file=./main 
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH      Symbols         FORTIFY Fortified      Fortifiable      FILE
No RELRO        No canary found   NX disabled   No PIE          No RPATH   No RUNPATH   No Symbols        No    0              0./main
```
