## **Enunciado**

Points: 500   
Country: Kazakhstan   
Attatchment: https://mega.nz/#!1tsFgIAR!JhnKO62d5jAcGvXM4pYsxbF5mMEyNz07UggP_e8lAEM   
Description: An evil rabbit has installed a nuclear bomb in the building and only a competitor like you, can defuse it and avoid its self-destruction. Be patient but please..DEFUSE THE BOMB!

## **Solución**

En este caso nos daba un binario que te pedía un pin para evitar que explotara una bomba:

```
file bomb-500 
bomb-500: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=a3990f9a0782759b97fc39aa38540656adc497c2, stripped

```
```
./bomb-500 

        .--``..---.                
         .````--:ohdmNms/`         
          -:/+++/-.:smNd+          
       ```..--:ohmNNdhh.           
     `-. `.``.-+sosshd.         :. 
   -os--/sosdmmNNMMNy         .+// 
  :h+.+hNNMMMNNNMMNm/      `/yNN.` 
 .do/oNNMMMMMmohs+:`    .+hNMMMM-` 
 `yohNhNNNMh-           dosNMMMmo- 
  -mN+hMMMy             .smNMNdd/+`
   yN.hMMh               +NMMNmhds:
   +N//m+                 .osshyho 
  ..smhh                           
   ::oNmy-                         
      .//yhs/:`                    
          :ymNN/                   
         .-+shdho.                 
             `.--..` '''   
   _______ ___ 
  | 7 | 8 | 9 |
  |___|___|___|
  | 4 | 5 | 6 |
  |___|___|___|
  | 1 | 2 | 3 |
  |___|___|___|
  | 0 | enter |
  |___|_______|
  Deactivation Code 
  > 1111 
BOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM!
       _.-^^---....,,--       
   _--                  --_   
  <                        >) 
  |                         | 
   ._                   _./  
      ```--. . , ; .--'''     
            | |   |           
         .-=||  | |=-.        
         `-=#$%&%$#=-'        
            | ;  :|           
   _____.,-#%&$@%#&#~,._____  

```

Con un strings no te mostraba nada interesante, había que ponerse a bucear en el desensamblado para ver si encontrabamos algo. Lo primero es averiguar el punto de entrada:

```
>>> set stop-on-solib-events 1
>>> info target
Symbols from "/root/Documents/FwhibbitCTF/reversing/bomb-500".
Local exec file:
	`/home/pericodelospalotes/FwhibbitCTF/reversing/bomb-500', file type elf64-x86-64.
	Entry point: 0x5555555555d0
```

A partir de ese punto de entrada llegamos a la función main:

```
0x000055555555591e
```

Esta es la primera parte del código donde metemos el pin:

```
    191e:	55                   	push   rbp
    191f:	48 89 e5             	mov    rbp,rsp
    1922:	41 54                	push   r12
    1924:	53                   	push   rbx
    1925:	48 81 ec d0 00 00 00 	sub    rsp,0xd0
    192c:	89 bd 2c ff ff ff    	mov    DWORD PTR [rbp-0xd4],edi
    1932:	48 89 b5 20 ff ff ff 	mov    QWORD PTR [rbp-0xe0],rsi
    1939:	e8 c2 fd ff ff       	call   1700 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x150>  <== Función que pinta el dibujito ASCII
    193e:	48 8d 35 2b 10 00 00 	lea    rsi,[rip+0x102b]        # 2970 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x13c0>
    1945:	48 8d 3d 14 29 20 00 	lea    rdi,[rip+0x202914]        # 204260 <_ZSt4cout@@GLIBCXX_3.4>
    194c:	e8 1f fb ff ff       	call   1470 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1951:	48 89 c2             	mov    rdx,rax
    1954:	48 8b 05 9d 26 20 00 	mov    rax,QWORD PTR [rip+0x20269d]        # 203ff8 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x202a48>
    195b:	48 89 c6             	mov    rsi,rax
    195e:	48 89 d7             	mov    rdi,rdx
    1961:	e8 aa fb ff ff       	call   1510 <_ZNSolsEPFRSoS_E@plt>
    1966:	48 8d 35 18 10 00 00 	lea    rsi,[rip+0x1018]        # 2985 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x13d5>
    196d:	48 89 c7             	mov    rdi,rax
    1970:	e8 fb fa ff ff       	call   1470 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1975:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
    197c:	48 89 c6             	mov    rsi,rax
    197f:	48 8d 3d ba 27 20 00 	lea    rdi,[rip+0x2027ba]        # 204140 <_ZSt3cin@@GLIBCXX_3.4>
    1986:	e8 45 fb ff ff       	call   14d0 <_ZStrsIcSt11char_traitsIcEERSt13basic_istreamIT_T0_ES6_PS3_@plt>   <== Función que lee el nº pin y lo almacena
    198b:	48 8d 85 70 ff ff ff 	lea    rax,[rbp-0x90]
    1992:	48 89 c7             	mov    rdi,rax
    1995:	e8 e6 fa ff ff       	call   1480 <strlen@plt>  <== Función que comprueba el tamaño del pin
    199a:	48 83 f8 08          	cmp    rax,0x8            <== El PIN tiene que tener 8 números
    199e:	74 05                	je     19a5 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x3f5>
```

Básicamente lo que hace todo esto es reservar memoria, guardar el pin introducido en memoria y comprobar que tenga 8 dígitos. En este caso he puesto de pin 11111111 que lo almacena en esta posición de memoria:

```
0x7fffffffe0f0:	0x31313131	0x31313131
```

