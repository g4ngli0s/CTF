## **Enunciado**

Tobacco Santa  
Description: Dr. Kringle has been recently trying to expand his joy-bringing business to the adult sector, but after seeing his latest startup we're not so sure if he's going in the right direction. Can you help him reconsider?

## **Solución**

Después de unas cuantas horas me di cuenta de que había que aplicar la técnica SROP.

- https://amriunix.com/post/sigreturn-oriented-programming-srop/

- https://blog.benroxbeecox.me/Binary-Exploitation/Rop-Advanced-Techniques/#sigreturn-oriented-programming

- https://anee.me/advanced-rop-techniques-16fd701909b5

- https://www.pwnthebox.net/reverse/engineering/and/binary/exploitation/series/2021/05/09/sigreturn-oriented-programming.html

- https://www.cs.vu.nl/~herbertb/papers/srop_sp14.pdf

- https://memn0ps.gitlab.io/XMAS-Pwn-Santa-Tobacco-Shop/


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
