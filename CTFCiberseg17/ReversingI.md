Este era un reto muy sencillo, simplemente había que ver el código ensamblador de la función "main" y ya tenías el flag:

```
00000000004004b6 <main>:
  4004b6:	55                   	push   rbp
  4004b7:	48 89 e5             	mov    rbp,rsp
  4004ba:	89 7d cc             	mov    DWORD PTR [rbp-0x34],edi
  4004bd:	48 89 75 c0          	mov    QWORD PTR [rbp-0x40],rsi
  4004c1:	c6 45 d0 66          	mov    BYTE PTR [rbp-0x30],0x66
  4004c5:	c6 45 d1 6c          	mov    BYTE PTR [rbp-0x2f],0x6c
  4004c9:	c6 45 d2 61          	mov    BYTE PTR [rbp-0x2e],0x61
  4004cd:	c6 45 d3 67          	mov    BYTE PTR [rbp-0x2d],0x67
  4004d1:	c6 45 d4 7b          	mov    BYTE PTR [rbp-0x2c],0x7b
  4004d5:	c6 45 d5 73          	mov    BYTE PTR [rbp-0x2b],0x73
  4004d9:	c6 45 d6 31          	mov    BYTE PTR [rbp-0x2a],0x31
  4004dd:	c6 45 d7 5f          	mov    BYTE PTR [rbp-0x29],0x5f
  4004e1:	c6 45 d8 6c          	mov    BYTE PTR [rbp-0x28],0x6c
  4004e5:	c6 45 d9 30          	mov    BYTE PTR [rbp-0x27],0x30
  4004e9:	c6 45 da 5f          	mov    BYTE PTR [rbp-0x26],0x5f
  4004ed:	c6 45 db 68          	mov    BYTE PTR [rbp-0x25],0x68
  4004f1:	c6 45 dc 34          	mov    BYTE PTR [rbp-0x24],0x34
  4004f5:	c6 45 dd 35          	mov    BYTE PTR [rbp-0x23],0x35
  4004f9:	c6 45 de 5f          	mov    BYTE PTR [rbp-0x22],0x5f
  4004fd:	c6 45 df 68          	mov    BYTE PTR [rbp-0x21],0x68
  400501:	c6 45 e0 33          	mov    BYTE PTR [rbp-0x20],0x33
  400505:	c6 45 e1 63          	mov    BYTE PTR [rbp-0x1f],0x63
  400509:	c6 45 e2 68          	mov    BYTE PTR [rbp-0x1e],0x68
  40050d:	c6 45 e3 30          	mov    BYTE PTR [rbp-0x1d],0x30
  400511:	c6 45 e4 5f          	mov    BYTE PTR [rbp-0x1c],0x5f
  400515:	c6 45 e5 63          	mov    BYTE PTR [rbp-0x1b],0x63
  400519:	c6 45 e6 30          	mov    BYTE PTR [rbp-0x1a],0x30
  40051d:	c6 45 e7 6e          	mov    BYTE PTR [rbp-0x19],0x6e
  400521:	c6 45 e8 5f          	mov    BYTE PTR [rbp-0x18],0x5f
  400525:	c6 45 e9 72          	mov    BYTE PTR [rbp-0x17],0x72
  400529:	c6 45 ea 34          	mov    BYTE PTR [rbp-0x16],0x34
  40052d:	c6 45 eb 64          	mov    BYTE PTR [rbp-0x15],0x64
  400531:	c6 45 ec 34          	mov    BYTE PTR [rbp-0x14],0x34
  400535:	c6 45 ed 72          	mov    BYTE PTR [rbp-0x13],0x72
  400539:	c6 45 ee 33          	mov    BYTE PTR [rbp-0x12],0x33
  40053d:	c6 45 ef 5f          	mov    BYTE PTR [rbp-0x11],0x5f
  400541:	c6 45 f0 68          	mov    BYTE PTR [rbp-0x10],0x68
  400545:	c6 45 f1 31          	mov    BYTE PTR [rbp-0xf],0x31
  400549:	c6 45 f2 67          	mov    BYTE PTR [rbp-0xe],0x67
  40054d:	c6 45 f3 68          	mov    BYTE PTR [rbp-0xd],0x68
  400551:	c6 45 f4 5f          	mov    BYTE PTR [rbp-0xc],0x5f
  400555:	c6 45 f5 66          	mov    BYTE PTR [rbp-0xb],0x66
  400559:	c6 45 f6 31          	mov    BYTE PTR [rbp-0xa],0x31
  40055d:	c6 45 f7 76          	mov    BYTE PTR [rbp-0x9],0x76
  400561:	c6 45 f8 33          	mov    BYTE PTR [rbp-0x8],0x33
  400565:	c6 45 f9 7d          	mov    BYTE PTR [rbp-0x7],0x7d
  400569:	c6 45 fa 00          	mov    BYTE PTR [rbp-0x6],0x0
  40056d:	5d                   	pop    rbp
  40056e:	c3                   	ret    
  40056f:	90                   	nop
```

