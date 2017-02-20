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
    19a5:	mov    DWORD PTR [rbp-0x14],0x0
    19ac:	cmp    DWORD PTR [rbp-0x14],0x7		<== Inicio del bucle (0..7)
    19b0:	jg     19df <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x42f>	<== Si es mayor que 7 se sale del bucle
    19b2:	mov    eax,DWORD PTR [rbp-0x14]
    19b5:	cdqe   
    19b7:	movzx  eax,BYTE PTR [rbp+rax*1-0x90]	<== Coge el siguiente dígito del pin (eax=pin[i])
    19bf:	cmp    al,0x39			<== Comprueba que el valor ASCII no sea mayor que 0x39 ('9')
    19c1:	jg     19d4 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x424> <== Nos manda al dibujito de la bomba si no se cumple la condición anterior
    19c3:	mov    eax,DWORD PTR [rbp-0x14]		
    19c6:	cdqe   
    19c8:	movzx  eax,BYTE PTR [rbp+rax*1-0x90] 	<== Vuelve a coger el mismo pin[i]
    19d0:	cmp    al,0x2f			<== Comprueba que el valor ASCII sea mayor que 0x2f ('/')
    19d2:	jg     19d9 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x429>
    19d4:	call   184b <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x29b>	<== Nos manda al dibujito de la bomba y sale del programa
    19d9:	add    DWORD PTR [rbp-0x14],0x1 <== i=i+1
    19dd:	jmp    19ac <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x3fc>
    
```
Una vez hechas las comprobaciones vamos a la pimera parte del meollo. Lo primero que hace es reservar memoria para copiar un patrón de caracteres. Este patrón de caracteres (le llamaremos Patron1) se usa para ofuscar (con operaciones lógicas) los valores del pin correcto.
```
    19f4:	call   1560 <_ZNSaIcEC1Ev@plt>
    19f9:	lea    rdx,[rbp-0x82]
    1a00:	lea    rax,[rbp-0xb0]
    1a07:	lea    rsi,[rip+0xf7c]        # 298a <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x13da>	<== Patron1 de caracteres que nos va a servir para ofuscar el pin (al menos 4 de los dígitos).
    1a0e:	mov    rdi,rax
    1a11:	call   1550 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEC1EPKcRKS3_@plt> 	<== Hace una copia del patron1 en otra posición de memoria.
    1a16:	lea    rax,[rbp-0x82]
    1a1d:	mov    rdi,rax
    1a20:	call   14e0 <_ZNSaIcED1Ev@plt>
```

Tendríamos el patron1 original y una copia del mismo, que vamos a usar para operar con nuestro pin introducido, en la siguientes posiciones de memoria respectivamente (va a ocupar 0x12 bytes):

```
>>> x/32xw 0x000055555555698a
0x55555555698a:	0x83b5fcf7	0x8983a781	0x9ebffdbd	0xf49aa6fa
0x55555555699a:	0x0000a284	0xa8bb0000	0xcad784ea	0xa9ee8080
>>> x/32xw 0x55555576b440
0x55555576b440:	0x83b5fcf7	0x8983a781	0x9ebffdbd	0xf49aa6fa
0x55555576b450:	0x0000a284	0x00000000	0x0001fbb1	0x00000000
```

Veamos las operaciones que hace el algoritmo en este bucle entre el pin introducido por nosotros y el patron1:

```
    1a25:	mov    QWORD PTR [rbp-0x20],0x0		<== i=0 (Asignación inicial, esta instrucción está fuera del bucle
    1a2d:	lea    rax,[rbp-0xb0]			<== Inicio del bucle. Sitio ideal para poner un breakpoint.
    1a34:	mov    rdi,rax				<== Mueve la posición de memoria de la copia del patron1 a $rdi
    1a37:	call   1420 <_ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE6lengthEv@plt>	<== Calcula tamaño de copia_patron1
    1a3c:	cmp    rax,QWORD PTR [rbp-0x20]		<== Comprueba si i=18 (longitud de copia_patron1)
    1a40:	seta   al
    1a43:	test   al,al
    1a45:	je     1a97 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x4e7>	<== Sale del bucle si i=18
    1a47:	mov    rdx,QWORD PTR [rbp-0x20]		<== Vuelve a traer valor de i
    1a4b:	lea    rax,[rbp-0xb0]			<== Valor de la posición de memoria que apunta a la copia del patron1
    1a52:	mov    rsi,rdx				<== Arg1=i
    1a55:	mov    rdi,rax				<== Arg2=&copia_patron1
    1a58:	call   1590 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt>	<== Calcula la posición de memoria de la copia del patron1 + i. Devuelve &copia_patron1+i. Es la forma de recorrer el patron1 byte a byte
    1a5d:	mov    rbx,rax				<== Guarda en $rbx &copia_patron1+i. $rbx=&copia_patron+i
    1a60:	movzx  r12d,BYTE PTR [rbx]		<== Guarda en r12 el valor copia_patron[i] 
    1a64:	mov    rax,QWORD PTR [rbp-0x30]		<== Trae la posición de memoria de nuestro pin introducido (&pin_introducido)
    1a68:	mov    rdi,rax
    1a6b:	call   1480 <strlen@plt>		<== Trae la longitud del pin (long=8)
    1a70:	mov    rcx,rax				<== $rcx=8
    1a73:	mov    rax,QWORD PTR [rbp-0x20]		<== $rax=i
    1a77:	mov    edx,0x0				<== Deja vacio $edx para recoger el resto de la siguiente división
    1a7c:	div    rcx				<== $rax=$rax/$rcx, el resto en $edx. j = i mod 8
    1a7f:	mov    rax,QWORD PTR [rbp-0x30]		<== $rax = &pin_introducido
    1a83:	add    rax,rdx				<== &pin_introducido=&pin_introducido+j
    1a86:	movzx  eax,BYTE PTR [rax]		<== Trae el valor pin[j] a $eax
    1a89:	not    eax				<== Not lógico del valor de pin[j]
    1a8b:	xor    eax,r12d				<== Xor lógico entre Not(pin[j]) y patron[i]. NuevoValor= Not(pin[j]) XOR patron[i]
    1a8e:	mov    BYTE PTR [rbx],al		<== Guarda nuevo valor en &copia_patron1+i. patron[i]=NuevoValor
    1a90:	add    QWORD PTR [rbp-0x20],0x1		<== i=i+1
    1a95:	jmp    1a2d <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x47d>
```
Ya se que están un poco liosos los comentarios en  el código, pero básicamente lo que hace este bucle es ofuscar el pin introducido en el patron1 realizando las siguientes operaciones:

```C
for (i=0; i < 18; i = i + 1) {
	j = i mod 8;
	copia_patron[i] = NOT(pin(j)) XOR copia_patron[i];
}
```

Así quedaría el patron1 después de realizar el bucle anterior con el pin 12345678:

```
0x55555576b440:	0x4b783539	0x44486d49	0x56723473	0x39516c32
0x55555576b450:	0x00006b4a	0x00000000	0x00000031	0x00000000
```	

Lo que sigue a continuación en el código es una serie de comprobaciones para ver si ciertos valores del pin introducido son correctos. Concretamente comprueba cuatro dígitos del pin, las posiciones 0x1, 0x8, 0xb, 0xe del patron1_codificado. Estas posiciones corresponden con los dígitos que se encuentran en las posiciones 1,0,3 y 6 del pin respectivamente. Tener en cuenta que la posición de cada dígito del pin se calcula haciendo el mod 8 con las posiciones del patron_codificado:

```
    1a97:	48 8d 85 50 ff ff ff 	lea    rax,[rbp-0xb0]
    1a9e:	48 89 c7             	mov    rdi,rax
    1aa1:	e8 8a fa ff ff       	call   1530 <_ZNKSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE5c_strEv@plt>
    1aa6:	48 89 45 c8          	mov    QWORD PTR [rbp-0x38],rax
    1aaa:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    1aae:	48 83 c0 01          	add    rax,0x1			<== Comprueba la posición 0x1 del patron_codificado
    1ab2:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1ab5:	3c 35                	cmp    al,0x35			<== La posicón 1 (0x1 mod 8) del pin está codificado con este valor 
    1ab7:	75 2d                	jne    1ae6 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x536>
    1ab9:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    1abd:	48 83 c0 08          	add    rax,0x8			<== Comprueba la posición 0x8 del patron_codificado
    1ac1:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1ac4:	3c 73                	cmp    al,0x73			<== La posicón 0 (0x8 mod 8) del pin está codificado con este valor
    1ac6:	75 1e                	jne    1ae6 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x536>
    1ac8:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    1acc:	48 83 c0 0b          	add    rax,0xb			<== Comprueba la posición 0xb del patron_codificado
    1ad0:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1ad3:	3c 56                	cmp    al,0x56			<== La posicón 3 (0xb mod 8) del pin está codificado con este valor
    1ad5:	75 0f                	jne    1ae6 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x536>
    1ad7:	48 8b 45 c8          	mov    rax,QWORD PTR [rbp-0x38]
    1adb:	48 83 c0 0e          	add    rax,0xe			<== Comprueba la posición 0xe del patron_codificado
    1adf:	0f b6 00             	movzx  eax,BYTE PTR [rax]
    1ae2:	3c 51                	cmp    al,0x51			<== La posicón 6 (0xe mod 8) del pin está codificado con este valor
    1ae4:	74 05                	je     1aeb <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x53b>
    1ae6:	e8 60 fd ff ff       	call   184b <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEE11_M_capacityEm@plt+0x29b>
```
De esta manera ya podemos saber esos cuatro valores del pin haciendo las operaciones inversas del bucle anterior, por ejemplo para la posición 1, el valor codificado tiene que ser 0x35. Por lo tanto,
patron_original[1]=0xfc; pin[1] = not(0xffffff35 XOR 0xfc) = 0x36 (6)
patron_original[8]=0xbd; pin[0] = not(0xffffff73 XOR 0xbc) = 0x31 (1)
patron_original[11]=0x9e; pin[3] = not(0xffffff56 XOR 0x9e) = 0x37 (7)
patron_original[14]=0x9a; pin[6] = not(0xffffff51 XOR 0x9a) = 0x34 (4)



