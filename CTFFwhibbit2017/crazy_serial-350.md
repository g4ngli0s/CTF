
## **Enunciado**

Crazy Serial  
Points: 350   
Country: Vongo - Kinshasa   
Attatchment: https://mega.nz/#!QpFSVYqI!85ekG2b5MwHW8BXxGvcUrkg_Liluz2M27c8xCeo4ZaA     
Description: Serial serial serials, I have nightmares with serials!!! Dear soldier, we need you to find the crazy serial for the rabbit team, the future of the team depends on you...GO GO GO!     

## **Solución**

Nos dan un binario que al ejecutarlo nos pide una dirección de correo y un número de serial:

```
./crazy_serial-350   
 Enter your Mail
 > aa@a 
 Enter Serial
 > 12345678
  Wrong Serial
```

Si hacemos un string sobre el binario nos puede ayudar para ver por donde empezar a buscar en el código ensamblador:

```
strings crazy_serial-350
 Wrong Serial
 Enter your Mail
 Enter Serial
  fwhibbit{
```

Lo primero de todo es averiguar el punto de entrada del binario, para poner un breakpoint en el inicio de la función principal:

```
>>> set stop-on-solib-events 1
>>> info target
Symbols from "/root/Documents/FwhibbitCTF/reversing/crazy_serial-350".
Local exec file:
	`/root/Documents/FwhibbitCTF/reversing/crazy_serial-350', file type elf64-x86-64.
	Entry point: 0x555555554e00
```
```
br *0x000055555555505c
```

Echemos un vistazo al código a ver que encontramos:

```
    1075:	call   f30                      <== Saca por pantalla el dibujo en ASCII del conejito playboy       
    107a:	lea    rdi,[rip+0x817]          
    1081:	mov    eax,0x0
    1086:	call   ce0 <printf@plt>         <== Saca por pantalla la cadena "Enter your Mail"
    108b:       lea    rax,[rbp-0x230]          <== Guarda la posición de memoria donde va a recoger el valor de Mail
    1092:	mov    rsi,rax			<== Carga $rsi con $rbp-0x230. $rsi se usa como origen en las operaciones con cadenas
    1095:	lea    rdi,[rip+0x201024]       <== Carga $rdi con el valor donde está la función _ZSt3cin que nos va a leer de consola
    109c:	call   d70                      <== Llama a la función para recoger y poner en memoria el valor de Mail (cin?)
```  
Una vez ejecutado lo anterior, vamos a tener el valor de nuestro Mail introducido (en este caso AA@A) en la siguiente posición de memoria:
```
>>> x/32xw $rbp-0x230
0x7fffffffdf40:	0x41404141	0x00000000	0x00000000	0x00000000
```

Si seguimos viendo el código, nos va a pedir el valor del serial y lo va a guardar en memoria:

```
    10a1:	lea    rdi,[rip+0x805]        
    10a8:	mov    eax,0x0
    10ad:	call   ce0 <printf@plt>		<== Saca por pantalla la cadena "Enter Serial"
    10b2:	lea    rax,[rbp-0x430]		<== Guarda la posición de memoria donde va a recoger el valor del Serial
    10b9:	mov    rsi,rax
    10bc:	lea    rdi,[rip+0x200ffd]        # 2020c0 <_ZSt3cin@@GLIBCXX_3.4>
    10c3:	call   d70 <_ZStrsIcSt11char_traitsIcEERSt13basic_istreamIT_T0_ES6_PS3_@plt>
```   
Si miramos la posición de memoria $rbp-0x430 es donde estará almacenado nuestro valor introducido como serial (en este caso 11111111):
```
>>> x/32xw $rbp-0x430
0x7fffffffdd40:	0x31313131	0x31313131	0xf7a7fb00	0x00007fff
```
Veamos ahora que comprobaciones hace con los valores introducidos. La primera comprobación la hace con Mail, va a recorrer la cadena con un bucle para comprobar si hay una '@' en la cadena. 


``` 
    10c8:	mov    DWORD PTR [rbp-0x18],0x0		<== i=0
    10cf:	mov    eax,DWORD PTR [rbp-0x18]		<== Inicio del bucle
    10d2:	movsxd rbx,eax
    10d5:	lea    rax,[rbp-0x230]
    10dc:	mov    rdi,rax
    10df:	call   d50 <strlen@plt>			<== Calcula la longitud de la cadena de Mail introducida
    10e4:	cmp    rbx,rax				<== Si ha llegado al último caracter de la cadena sale
    10e7:	jae    1104 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x324>
    10e9:	mov    eax,DWORD PTR [rbp-0x18]
    10ec:	cdqe   
    10ee:	movzx  eax,BYTE PTR [rbp+rax*1-0x230]
    10f6:	cmp    al,0x40				<== Comprueba que el caracter[i] de Mail sea igual a @
    10f8:	jne    10fe <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x31e>
    10fa:	mov    BYTE PTR [rbp-0x11],0x1		<== Si hay una @ se guarda un 1 en var_11(=$rbp-0x11) -- Centinela
    10fe:	add    DWORD PTR [rbp-0x18],0x1		<== i++
    1102:	jmp    10cf <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x2ef> 	<== Vuelve al principio del bucle
    
``` 
También comprueba que Mail sea mayor que 3 caracteres:
```  
    1104:	movzx  eax,BYTE PTR [rbp-0x11]
    1108:	xor    eax,0x1
    110b:	test   al,al
    110d:	jne    1124 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x344>
    110f:	lea    rax,[rbp-0x230]
    1116:	mov    rdi,rax
    1119:	call   d50 <strlen@plt>
    111e:	cmp    rax,0x3
    1122:	ja     1129 <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x349>
    1124:	call   100f <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x22f>
```

