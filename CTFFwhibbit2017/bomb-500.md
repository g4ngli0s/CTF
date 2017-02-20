## **Enunciado**

Points: 500   
Country: Kazakhstan   
Attatchment: https://mega.nz/#!1tsFgIAR!JhnKO62d5jAcGvXM4pYsxbF5mMEyNz07UggP_e8lAEM   
Description: An evil rabbit has installed a nuclear bomb in the building and only a competitor like you, can defuse it and avoid its self-destruction. Be patient but please..DEFUSE THE BOMB!

## **Solución**

En este caso nos daba un binario que te pedía un pin para desactivar una bomba (Jack Bauer powa):

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
br *0x000055555555591e
```

Esta es la primera parte del código donde metemos el pin:

```
    191e:	push   rbp
    191f:	mov    rbp,rsp
    1922:	push   r12
    1924:	push   rbx
    1925:	sub    rsp,0xd0
    192c:	mov    DWORD PTR [rbp-0xd4],edi
    1932:	mov    QWORD PTR [rbp-0xe0],rsi
    1939:	call   1700 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x150>  <== Función que pinta el dibujito ASCII
    193e:	lea    rsi,[rip+0x102b]        # 2970 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x13c0>
    1945:	lea    rdi,[rip+0x202914]        # 204260 <_ZSt4cout@@GLIBCXX_3.4>
    194c:	call   1470 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1951:	mov    rdx,rax
    1954:	mov    rax,QWORD PTR [rip+0x20269d]        # 203ff8 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x202a48>
    195b:	mov    rsi,rax
    195e:	mov    rdi,rdx
    1961:	call   1510 <_ZNSolsEPFRSoS_E@plt>
    1966:	lea    rsi,[rip+0x1018]        # 2985 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x13d5>
    196d:	mov    rdi,rax
    1970:	call   1470 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
    1975:	lea    rax,[rbp-0x90]
    197c:	mov    rsi,rax
    197f:	lea    rdi,[rip+0x2027ba]        # 204140 <_ZSt3cin@@GLIBCXX_3.4>
    1986:	call   14d0 <_ZStrsIcSt11char_traitsIcEERSt13basic_istreamIT_T0_ES6_PS3_@plt>   <== Función que lee el nº pin y lo almacena
    198b:	lea    rax,[rbp-0x90]
    1992:	mov    rdi,rax
    1995:	call   1480 <strlen@plt>  <== Función que comprueba el tamaño del pin
    199a:	cmp    rax,0x8            <== El PIN tiene que tener 8 números
    199e:	je     19a5 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x3f5>
```

Básicamente lo que hace todo esto es reservar memoria, guardar el pin introducido en memoria y comprobar que tenga 8 dígitos. En este caso he puesto de pin 11111111 que lo almacena en esta posición de memoria:

```
0x7fffffffe0f0:	0x31313131	0x31313131
```

Una vez superado que el pin sea de 8 dígitos, hay un bucle en el que recorre cada dígito del pin para comprobar que sea un número y no cualquier otro carácter inválido:

```
    19a5:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [rbp-0x14],0x0
    19ac:	83 7d ec 07          	cmp    DWORD PTR [rbp-0x14],0x7		<== Inicio del bucle (0..7)
    19b0:	7f 2d                	jg     19df <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x42f>	<== Si es mayor que 7 se sale del bucle
    19b2:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]
    19b5:	48 98                	cdqe   
    19b7:	0f b6 84 05 70 ff ff ff 	movzx  eax,BYTE PTR [rbp+rax*1-0x90]	<== Coge el siguiente dígito del pin (eax=pin[i])
    19bf:	3c 39                	cmp    al,0x39			<== Comprueba que el valor ASCII no sea mayor que 0x39 ('9')
    19c1:	7f 11                	jg     19d4 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x424> <== Nos manda al dibujito de la bomba si no se cumple la condición anterior
    19c3:	8b 45 ec             	mov    eax,DWORD PTR [rbp-0x14]		
    19c6:	48 98                	cdqe   
    19c8:	0f b6 84 05 70 ff ff ff 	movzx  eax,BYTE PTR [rbp+rax*1-0x90] 	<== Vuelve a coger el mismo pin[i]
    19d0:	3c 2f                	cmp    al,0x2f			<== Comprueba que el valor ASCII sea mayor que 0x2f ('/')
    19d2:	7f 05                	jg     19d9 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x429>
    19d4:	e8 72 fe ff ff       	call   184b <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x29b>	<== Nos manda al dibujito de la bomba y sale del programa
    19d9:	83 45 ec 01          	add    DWORD PTR [rbp-0x14],0x1 <== i=i+1
    19dd:	eb cd                	jmp    19ac <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x3fc>
    
```
Una vez hechas las comprobaciones vamos a la pimera parte del meollo. 


