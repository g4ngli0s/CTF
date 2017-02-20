## **Enunciado**

How Many Rabbits  
Points: 200   
Country: Morroco  
Attatchment: https://mega.nz/#!N4dDVSYY!mcH-FyRD9cwCuL8i3OFy_1zrA55djoLk9s2Qd7-hPuo   
Description: We need the information in this binary password protected...can you help us?

## **Solución**

Este binario es muy parecido al de 150 puntos, pero aquí añadía la dificultad de encontrar el 'entrypoint' del programa para poder insertar un breakpoint en ese punto para iniciar el reversing. Veamos como se hace con gdb:

```
gdb-peda$ set stop-on-solib-events 1
gdb-peda$ info target
Symbols from "/root/Documents/FwhibbitCTF/Reversing/rabbits-200".
Local exec file:
	`/home/pericodelospalotes/FwhibbitCTF/Reversing/rabbits-200', file type elf64-x86-64.
	Entry point: 0x555555554de0
```

Aquí vemos guardar en el stack frame algunos valores sospechosos

```
     b31:	mov    ecx,0x6f77                   <== Cadena 'ow'
     b36:	mov    eax,0x6867                   <== Cadena 'hg'
     b3b:	mov    edx,0x7774                   <== Cadena 'wt'
     b40:	mov    esi,0x7774                   <== Cadena 'wt'
     b45:	sub    rsp,0x220
     b4c:	mov    WORD PTR [rsp+0x30],cx
     b51:	mov    WORD PTR [rsp+0x10],ax
     b56:	lea    rbx,[rsp+0x120]
     b5e:	mov    WORD PTR [rsp+0x20],dx
     b63:	mov    WORD PTR [rsp+0xf0],si
     b6b:	mov    DWORD PTR [rsp+0x50],0x
     b73:	mov    DWORD PTR [rsp+0x60],0x357431	<== Cadena '5t1'
     b7b:	mov    BYTE PTR [rsp+0x12],0x0
     b80:	mov    DWORD PTR [rsp+0x70],0x77745f	<== Cadena 'wt_'
     b88:	mov    DWORD PTR [rsp+0x80],0x79746e	<== Cadena 'ytn'
     b93:	mov    BYTE PTR [rsp+0x22],0x0
     b98:	mov    DWORD PTR [rsp+0x90],0x725f30	<== Cadena 'r_0'
     ba3:	mov    DWORD PTR [rsp+0xa0],0x72615f	<== Cadena 'ra_'
     bae:	mov    BYTE PTR [rsp+0x32],0x0
     bb3:	mov    DWORD PTR [rsp+0xb0],0x746e65	<== Cadena 'tne'
     bbe:	mov    DWORD PTR [rsp+0xf2],0x746e65	<== Cadena 'tne'
     bc9:	call    sub_F10				<== Función que hace el dibujo en ASCII del conejo
```

Y en esta parte del código vemos como construye la cadena que va a servir de password y la pone en donde apunta $rsi

```
=> 0x555555554c0b:	call   0x555555554ad0 <_ZStrsIcSt11char_traitsIcEERSt13basic_istreamIT_T0_ES6_PS3_@plt>
   0x555555554c10:	mov    eax,DWORD PTR [rsp+0x50]
   0x555555554c14:	lea    rsi,[rsp+0xf0]
   0x555555554c1c:	mov    rdi,rbx
   0x555555554c1f:	mov    DWORD PTR [rsp+0xf5],eax
   0x555555554c26:	movzx  eax,WORD PTR [rsp+0x30]
   0x555555554c2b:	mov    WORD PTR [rsp+0xf8],ax
   0x555555554c33:	movzx  eax,BYTE PTR [rsp+0x32]
   0x555555554c38:	mov    BYTE PTR [rsp+0xfa],al
=> 0x555555554c3f:	call   0x555555554af0 <strcmp@plt>
   0x555555554c44:	test   eax,eax
```

Esto es los valores que van cogiendo los registros hasta completar la palabra:

```
RAX: 0x6f77 ('wo')
RAX: 0x745f79 ('y_t')
RSI: 0x7fffffffe050 --> 0x746e657774 ('twent')
....
RSI: 0x7fffffffe050 ("twenty_two")
RDI: 0x7fffffffe080 --> 0x41414141 ('AAAA')
```


Y aquí como se ve en memoria:

```
gdb-peda$ x/32xw $rsi
0x7fffffffe050:	0x6e657774	0x745f7974	0x00006f77	0x00000000
```

Ejecutamos y nos devuelve la flag:

```
./rabbits-200 

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

 one rabbit, two rabbit... 
 > twenty_two

fwhibbit{Tw3nty_tw0_r4bb1t5_ar3_en0ugh} 
```

