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
     call    sub_F10

.text:0000000000000B30 push    rbx
.text:0000000000000B31 mov     ecx, 6F77h
.text:0000000000000B36 mov     eax, 6867h
.text:0000000000000B3B mov     edx, 7774h
.text:0000000000000B40 mov     esi, 7774h
.text:0000000000000B45 sub     rsp, 220h
.text:0000000000000B4C mov     [rsp+228h+var_1F8], cx
.text:0000000000000B51 mov     [rsp+228h+var_218], ax
.text:0000000000000B56 lea     rbx, [rsp+228h+s1]
.text:0000000000000B5E mov     [rsp+228h+var_208], dx
.text:0000000000000B63 mov     word ptr [rsp+228h+s2], si
.text:0000000000000B6B mov     [rsp+228h+var_1D8], 745F79h
.text:0000000000000B73 mov     [rsp+228h+var_1C8], 357431h
.text:0000000000000B7B mov     [rsp+228h+var_216], 0
.text:0000000000000B80 mov     [rsp+228h+var_1B8], 77745Fh
.text:0000000000000B88 mov     [rsp+228h+var_1A8], 79746Eh
.text:0000000000000B93 mov     [rsp+228h+var_206], 0
.text:0000000000000B98 mov     [rsp+228h+var_198], 725F30h
.text:0000000000000BA3 mov     [rsp+228h+var_188], 72615Fh
.text:0000000000000BAE mov     [rsp+228h+var_1F6], 0
mov     [rsp+228h+var_178], 746E65h
mov     [rsp+228h+var_136], 746E65h




=> 0x555555554c0b:	call   0x555555554ad0 <_ZStrsIcSt11char_traitsIcEERSt13basic_istreamIT_T0_ES6_PS3_@plt>
   0x555555554c10:	mov    eax,DWORD PTR [rsp+0x50]
   0x555555554c14:	lea    rsi,[rsp+0xf0]
   0x555555554c1c:	mov    rdi,rbx
   0x555555554c1f:	mov    DWORD PTR [rsp+0xf5],eax
   0x555555554c26:	movzx  eax,WORD PTR [rsp+0x30]
=> 0x555555554c2b:	mov    WORD PTR [rsp+0xf8],ax
   0x555555554c33:	movzx  eax,BYTE PTR [rsp+0x32]
   0x555555554c38:	mov    BYTE PTR [rsp+0xfa],al
   0x555555554c3f:	call   0x555555554af0 <strcmp@plt>
   0x555555554c44:	test   eax,eax


RAX: 0x6f77 ('wo')
RAX: 0x745f79 ('y_t')
RSI: 0x7fffffffe050 --> 0x746e657774 ('twent')


c10:	8b 44 24 50          	mov    eax,DWORD PTR [rsp+0x50]
     c14:	48 8d b4 24 f0 00 00 00 	lea    rsi,[rsp+0xf0]
     c1c:	48 89 df             	mov    rdi,rbx
     c1f:	89 84 24 f5 00 00 00 	mov    DWORD PTR [rsp+0xf5],eax
     c26:	0f b7 44 24 30       	movzx  eax,WORD PTR [rsp+0x30]
     c2b:	66 89 84 24 f8 00 00 00 	mov    WORD PTR [rsp+0xf8],ax
     c33:	0f b6 44 24 32       	movzx  eax,BYTE PTR [rsp+0x32]
     c38:	88 84 24 fa 00 00 00 	mov    BYTE PTR [rsp+0xfa],al
     c3f:	e8 ac fe ff ff       	call   af0 <strcmp@plt>
     c44:	85 c0                	test   eax,eax
```
