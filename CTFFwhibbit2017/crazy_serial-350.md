
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
    10ee:	movzx  eax,BYTE PTR [rbp+rax*1-0x230]	<== Coge el caracter[i] de Mail
    10f6:	cmp    al,0x40				<== Comprueba que el caracter[i] de Mail sea igual a @
    10f8:	jne    10fe <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x31e>
    10fa:	mov    BYTE PTR [rbp-0x11],0x1		<== Si hay una @ se guarda un 1 en var_11(=$rbp-0x11) -- Centinela
    10fe:	add    DWORD PTR [rbp-0x18],0x1		<== i++
    1102:	jmp    10cf <_ZNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEixEm@plt+0x2ef> 	<== Vuelve al principio del bucle
    
``` 
También comprueba que Mail sea mayor que 3 caracteres:
```  
    1104:	movzx  eax,BYTE PTR [rbp-0x11]	<== Recoge valor del centinela
    1108:	xor    eax,0x1			<== Comprueba si centinela es 1 (si hay una @)
    110b:	test   al,al				
    110d:	jne    1124 			<== Sale si el centinela=0
    110f:	lea    rax,[rbp-0x230]		<== Vuelve a coger el valor de &Mail
    1116:	mov    rdi,rax
    1119:	call   d50 <strlen@plt>		<== Calcula la longitud de Mail
    111e:	cmp    rax,0x3			<== Comprueba si tiene más de 3 caracteres
    1122:	ja     1129 			<== Sigue la ejecucción si lenght(Mail)>3
    1124:	call   100f 			<== Función que llama a salir del programa si no cumple alguna de las condiciones
```

Una vez superado el Mail, empieza la locura de comprobaciones con el Serial, hay una ristra enorme de comprobaciones y creo que no voy a poner todas, pondré las más significativas. Se trata de ir superando todas las comprobaciones hasta sacar el valor del serial. La primera comprobación es el nº de dígitos que tiene el serial:

```
    1129:	lea    rax,[rbp-0x430]	<== Posición de memoria de Serial
    1130:	mov    rdi,rax
    1133:	call   d50 <strlen@plt>	<== Halla length(Serial)
    1138:	cmp    rax,0x18		<== Compara con 24
    113c:	ja     1143 		<== Si es mayor que 24 sigue
    113e:	call   100f 		<== Si no lo es sale
```
Comprueba que en las posiciones 0x5, 0xb y 0x12 el Serial tenga el caracter "-".
```
    1143:	movzx  eax,BYTE PTR [rbp-0x42b]		<== Posicion 5 del Serial ($rbp-0x430 es la posición 0)
    114a:	cmp    al,0x2d				<== Valor ASCII de '-'
    114c:	je     1169 
    114e:	movzx  eax,BYTE PTR [rbp-0x425]		<== Posición 0xb del Serial(0x430-0x425 = 0xb)
    1155:	cmp    al,0x2d				<== Valor ASCII de '-'
    1157:	je     1169 
    1159:	movzx  eax,BYTE PTR [rbp-0x41e]		<== Posición 0xb del Serial(0x430-0x41e = 0x12)
    1160:	cmp    al,0x2d				<== Valor ASCII de '-'
    1162:	je     1169 
    1164:	call   100f 
```
La siguiente comprobación es que las posiciones 0x0 y 0xa del Serial sean iguales, Serial[0x0]=Serial[0xa]:

```
    1169:	0f b6 95 d0 fb ff ff 	movzx  edx,BYTE PTR [rbp-0x430]	<== 0x430-0x430 -> Posición 0x0
    1170:	0f b6 85 da fb ff ff 	movzx  eax,BYTE PTR [rbp-0x426] <== 0x430-0x426 -> Posición 0xa
    1177:	38 c2                	cmp    dl,al
    1179:	74 05                	je     1180 
    117b:	e8 8f fe ff ff       	call   100f 
```
Si seguimos el ensamblador se tiene que cumplir lo siguiente:

```
1187 cmp     al, 7Ah : 	Serial[0x1] = 0x7a ('z')
1197 cmp     al, 79h : 	Serial[0x3] = 0x79 ('y')
11A7 test    al, al  : 	Serial[0x19] = 0x00 (Último caracter de Serial, indica fin de cadena)
11B7 cmp     al, 65h : 	Serial[0x2] = 0x65 ('e')
11D7 cmp     eax, edx: 	Serial[0x4] = Serial[0x11]+0x2
11E7 cmp     al, 64h :	Serial[0x6] = 0x64 ('d')
11F7 cmp     al, 72h :  Serial[0x7] = 0x72 ('r')
120E cmp     dl, al  :	Serial[0x8] = Serial[0x16]
121E cmp     al, 4ch :  Serial[0x9] = 0x4c ('L')
1244 call    sub_1029:  Serial[0xc] = Serial[0x5]+Serial[0x5]+0x9
126C cmp     eax, edx:  Serial[0x17] = Serial[0x11]+0x1
127C cmp     al, 74h :  Serial[0xd] = 0x74 ('t')
128C cmp     al, 66h :  Serial[0xe] = 0x66 ('f')
12B2 call    sub_1029: 	Serial[0x10] = Serial[0xf]+Serial[0xf]+0xFFFFFF7A
12CA cmp     al, 54h :  Serial[0x15] = 0x54 ('T')
12DA cmp     al, 48h : 	Serial[0x10] = 0x48 ('H')
12EA cmp     al, 75h :	Serial[0x14] = 0x48 ('u')
12FA cmp     al, 35h :	Serial[0x11] = 0x35 ('5')
130A cmp     al, 70h : 	Serial[0x13] = 0x70 ('p')
131A cmp     al, 46h :	Serial[0x16] = 0x46 ('F')
1331 cmp     dl, al  :	Serial[0xa] = Serial[0x15]
1357 call    sub_1029:	Serial[0x14] = Serial[0x18]+Serial[0x18]+0xFFFFFFC3
```

Si lo ponemos todo en orden y lo ejecutamos tenemos la flag:

```
fwhibbit{r4bb1t_s3r14l-2JBH8tckcTj}
```
	
	
