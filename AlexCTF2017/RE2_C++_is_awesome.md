
Datos del ejecutable que nos proporcionan:

```
file ./re2 
./re2: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=08fba98083e7c1f7171fd17c82befdfe1dcbcc82, stripped
```

Si lo ejecutamos nos encontramos con el clásico archivo que hay que pasarle un valor para averiguar el flag:

```
~/Documents/AlexCTF/reversing# ./re2 
Usage: ./re2 flag
```

Lo primero de todo es empezar con strings a ver si nos da alguna pista de por donde encaminarnos para resolver el reto.

```
strings ./re2 
[]A\A]A^A_
L3t_ME_T3ll_Y0u_S0m3th1ng_1mp0rtant_A_{FL4G}_W0nt_b3_3X4ctly_th4t_345y_t0_c4ptur3_H0wev3r_1T_w1ll_b3_C00l_1F_Y0u_g0t_1t
Better luck next time
You should have the flag by now
Usage: 
 flag
;*3$"
zPLR
GCC: (GNU) 6.1.1 20160721 (Red Hat 6.1.1-4)
GCC: (GNU) 6.2.1 20160916 (Red Hat 6.2.1-2)
```


El punto de entrada según IDA está en la posición 0x0000000000400A60, donde colocaremos un breakpoint. Si seguimos la ejecucción vemos que ejecuta las librerias del sistema para cargar el ejecutable en memoria (__libc_start_main) y al final del todo llama al punto de entrada real de nuestro programa (0x0000000000400B89):

```
0x00007ffff71c023e __libc_start_main+126 call   rbp
.....
0x0000000000400dec ? call   0x400960
...
0x0000000000400960 ? sub    rsp,0x8
0x0000000000400964 ? mov    rax,QWORD PTR [rip+0x201685]        # 0x601ff0
0x000000000040096b ? test   rax,rax
0x000000000040096e ? je     0x400972
0x0000000000400970 ? call   rax
.....

```

En vez de pasar por todo este proceso tedioso, se puede ir directamente al strings y ver en IDA desde dónde se llama a la string "Usage" por ejemplo y partir de ahí hacía arriba para ver el punto de entrada y poner un breakpoint ahí:

```
br *0x0000000000400B89
```

A partír de aquí lo primero que nos encontramos es con una comprobación del número de argumentos que hemos pasado al programa. En este caso el número de argumento deben ser dos, que corresponden al nombre del programa en sí (argumento 1) y el texto que introduzcamos como intento de flag (argumento 2).

```
0x0000000000400b92 ? mov    DWORD PTR [rbp-0x64],edi   	<--- rdi contiene el número de parámetros que se le han pasado al programa (2)
0x0000000000400b95 ? mov    QWORD PTR [rbp-0x70],rsi
0x0000000000400b99 ? cmp    DWORD PTR [rbp-0x64],0x2 	<--- Aquí comprueba que le pases un argumento el programa. Si no es igual a 2 sigue al mensaje de usage (0x400b9f)
0x0000000000400b9d ? je     0x400bd7
0x0000000000400b9f ? mov    rax,QWORD PTR [rbp-0x70]
0x0000000000400ba3 ? mov    rbx,QWORD PTR [rax]
0x0000000000400ba6 ? mov    esi,0x400f09				<--- Offset de  "Usage: "
0x0000000000400bab ? mov    edi,0x602140				<--- Offset de std::cout
0x0000000000400bb0 ? call   0x4009d0 <_ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_PKc@plt>
```


Siguiendo la ejecución del programa, reserva espacio y coloca nuestro argumento en memoria. Una vez hecho esto tenemos el bucle principal del programa. Lo que va a hacer en este bucle básicamente es ir comparando la cadena introducida por nosotros con los caracteres del flag. Lo importante a destacar es que los caracteres del flag no va a estar correlativos, sino se hubieran podido ver con el comando strings, sino que van a estar camuflados dentro de la memoria y vamos a acceder a ellos utilizando un array de offsets. Veamos un ejemplo de manera práctica:

Caracteres de nuestro flag desordenados en memoria:

```
x/64xw 0x400e58
0x400e58:	0x5f74334c	0x545f454d	0x5f6c6c33	0x5f753059
0x400e68:	0x336d3053	0x6e316874	0x6d315f67	0x74723070
0x400e78:	0x5f746e61	0x467b5f41	0x7d47344c	0x6e30575f
0x400e88:	0x33625f74	0x3458335f	0x796c7463	0x3468745f
0x400e98:	0x34335f74	0x745f7935	0x34635f30	0x72757470
0x400ea8:	0x30485f33	0x33766577	0x54315f72	0x6c31775f
0x400eb8:	0x33625f6c	0x3030435f	0x46315f6c	0x7530595f
0x400ec8:	0x7430675f	0x0074315f	0x74746542	0x6c207265
0x400ed8:	0x206b6375	0x7478656e	0x6d697420	0x00000a65
0x400ee8:	0x20756f59	0x756f6873	0x6820646c	0x20657661
0x400ef8:	0x20656874	0x67616c66	0x20796220	0x0a776f6e
0x400f08:	0x61735500	0x203a6567	0x6c662000	0x000a6761
0x400f18:	0x3b031b01	0x00000074	0x0000000d	0xfffffa68
0x400f28:	0x000000c0	0xfffffb48	0x00000090	0xfffffc3e
0x400f38:	0x000000e8	0xfffffc5b	0x00000108	0xfffffc71
0x400f48:	0x00000148	0xfffffdd2	0x000001f0	0xfffffe10
```

Matriz de offsets en memoria:

```
0x6020c0:	0x00000024	0x00000000	0x00000005	0x00000036
0x6020d0:	0x00000065	0x00000007	0x00000027	0x00000026
0x6020e0:	0x0000002d	0x00000001	0x00000003	0x00000000
0x6020f0:	0x0000000d	0x00000056	0x00000001	0x00000003
0x602100:	0x00000065	0x00000003	0x0000002d	0x00000016
0x602110:	0x00000002	0x00000015	0x00000003	0x00000065
0x602120:	0x00000000	0x00000029	0x00000044	0x00000044
0x602130:	0x00000001	0x00000044	0x0000002b	0x00000000
```

Si queremos acceder al primer caracter del flag (indice=0), primero habrá que irse a la posición del array de offsets(0x6020c0) + indice(0), eso corresponde al valor 0x24. Este valor será nuestro offset para hallar el primer carácter del flag en memoria, en este caso 0x400e58 + 0x24 = 0x400e7c, que corresponde casualmente a la letra "A". Y como nuestro formato de flag es ALEXCTF{loquesea} tiene pinta de que vamos bien encaminados. Si seguimos el mismo procedimiento, los siguientes caracteres serían: 4c 45 58 43 54 46 7b 57 33 5f 4c 30 76 33 5f 43 5f 57 31 74 68 5f 43 4c 34 35 35 33 35 7d. Que se corresponde con el flag que buscábamos: ALEXCTF{W3_L0v3_C_W1th_CL45535}

Aquí se puede ver el mismo procedimiento en código ensamblador:

```
0x0000000000400c24 ? lea    rax,[rbp-0x50] 		<--- Inicio del bucle
0x0000000000400c28 ? mov    rdi,rax
0x0000000000400c2b ? call   0x4009f0 			<--- Función que nos da la posición del siguiente carácter de la cadena introducida por nosotros como segundo parámetro
0x0000000000400c30 ? mov    QWORD PTR [rbp-0x20],rax
0x0000000000400c34 ? lea    rdx,[rbp-0x20]
0x0000000000400c38 ? lea    rax,[rbp-0x60]
0x0000000000400c3c ? mov    rsi,rdx
0x0000000000400c3f ? mov    rdi,rax				
0x0000000000400c42 ? call   0x400d3d			<--- Función que nos determina si ya hemos leído todos los caracteres de la cadena introducida por nosotros (índice del bucle)
0x0000000000400c47 ? test   al,al				<--- Si es 0, ya hemos leído todo y salimos.
0x0000000000400c49 ? je     0x400c95			<--- Salto fuera del bucle si es igual a 0
0x0000000000400c4b ? lea    rax,[rbp-0x60]
0x0000000000400c4f ? mov    rdi,rax
0x0000000000400c52 ? call   0x400d9a			<--- Función que nos devuelve la posición de memoria del siguiente cáracter introducido por nosotros
0x0000000000400c57 ? movzx  edx,BYTE PTR [rax]	<--- Mueve a edx el siguiente caracter de la cadena introducida por nosotros
0x0000000000400c5a ? mov    rcx,QWORD PTR [rip+0x20143f]        <--- Posición de memoria donde están guardados los caracteres del flag
0x0000000000400c61 ? mov    eax,DWORD PTR [rbp-0x14]	<--- Recupera el índice del bucle que se guarda en rbp-0x14 (variable local)
0x0000000000400c64 ? cdqe   
0x0000000000400c66 ? mov    eax,DWORD PTR [rax*4+0x6020c0]	<--- Matriz de offset en memoria con los valores que vamos a ir tomando para leer los caracteres del flag
0x0000000000400c6d ? cdqe   
0x0000000000400c6f ? add    rax,rcx				<--- Posición correspondiente al siguiente caracter de la flag, calculado según la posición fija y el offset tomado
0x0000000000400c72 ? movzx  eax,BYTE PTR [rax]
0x0000000000400c75 ? cmp    dl,al
0x0000000000400c77 ? setne  al
0x0000000000400c7a ? test   al,al
0x0000000000400c7c ? je     0x400c83
0x0000000000400c7e ? call   0x400b56
0x0000000000400c83 ? add    DWORD PTR [rbp-0x14],0x1	<--- Aumenta en uno el índice
0x0000000000400c87 ? lea    rax,[rbp-0x60]
0x0000000000400c8b ? mov    rdi,rax
0x0000000000400c8e ? call   0x400d7a			<--- Función que aumenta en 1 la dirección de la cadena introducida por nosotros (para apuntar al siguiente caracter)
0x0000000000400c93 ? jmp    0x400c24 			<--- Vuelve al inicio del bucle

0x0000000000400c95 ? call   0x400b73
0x0000000000400c9a ? mov    ebx,0x0
0x0000000000400c9f ? lea    rax,[rbp-0x50]
```

Eso es todo y recordad que estas posiciones de memoria serán diferentes en nuestro ordenador. Si queréis ver todo el código completo en ensamblador, objdump es vuestro amigo:

```
objdump -M intel -S ./re2
```
