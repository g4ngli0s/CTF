
#### Enunciado

If I tell you what version of python I used .. where is the fun in that?

#### Solución 1 (larga)

En este caso nos proporcionan un archivo pre-compilado en python "unvm_me.pyc". Lo decompilamos con cualquiera de las herramientas que hay disponibles, yo he usado "easypythondecompiler" y nos da el siguiente código:

```python
# Embedded file name: unvm_me.py
import md5
md5s = [174282896860968005525213562254350376167L,
 137092044126081477479435678296496849608L,
 126300127609096051658061491018211963916L,
 314989972419727999226545215739316729360L,
 256525866025901597224592941642385934114L,
 115141138810151571209618282728408211053L,
 8705973470942652577929336993839061582L,
 256697681645515528548061291580728800189L,
 39818552652170274340851144295913091599L,
 65313561977812018046200997898904313350L,
 230909080238053318105407334248228870753L,
 196125799557195268866757688147870815374L,
 74874145132345503095307276614727915885L]
print 'Can you turn me back to python ? ...'
flag = raw_input('well as you wish.. what is the flag: ')
if len(flag) > 69:
    print 'nice try 1'
    exit()
if len(flag) % 5 != 0:
    print 'nice try 2'
    exit()
for i in range(0, len(flag), 5):
    s = flag[i:i + 5]
    if int('0x' + md5.new(s).hexdigest(), 16) != md5s[i / 5]:
        print 'nice try 3'
        exit()

print 'Congratz now you have the flag'
```

Si seguimos un poco el código nos dan un array de md5s en valor decimal. Cada uno de los valores se corresponde con el md5 de cinco caracteres del flag. Se trata de comparar los md5 de todas las posibles combinaciones de cinco caracteres(del tipo mayúsculas, minúsculas, números y caracteres especiales) con el array de md5s y colocar los resultados en el orden del array. 

En esta solución me compliqué la vida creando un diccionario(nada menos que de 5Gigas) con crunch con todas las posibles combinaciones de caracteres tomados de 5 en 5:

```
crunch 5 5 -f /usr/share/crunch/charset.lst mixalpha-numeric  -o dicc.txt
```
Nota: En mixalpha-numeric añadí los caracteres "_", "{" y "}"

Luego le pase un script en python que me dio la colección de caracteres del flag:

```python
import md5

md5s = [174282896860968005525213562254350376167L,
 137092044126081477479435678296496849608L,
 126300127609096051658061491018211963916L,
 314989972419727999226545215739316729360L,
 256525866025901597224592941642385934114L,
 115141138810151571209618282728408211053L,
 8705973470942652577929336993839061582L,
 256697681645515528548061291580728800189L,
 39818552652170274340851144295913091599L,
 65313561977812018046200997898904313350L,
 230909080238053318105407334248228870753L,
 196125799557195268866757688147870815374L,
 74874145132345503095307276614727915885L]

infile = open('dicc.txt','r')

for line in infile:
	var1 = int('0x' + md5.new(line.rstrip('\n')).hexdigest(),16)
	for i in range(0,len(md5s)):
		var2 = md5s[i]
		if var1 == var2:
			print(line)

infile.close()

```

El resultado después de media hora de ejecucción:

ALEXCTF{dv5d4s2vj8nk43s8d8l6m1n5l67ds9v41n52nv37j481h3d28n4b6v3k}


#### Solución 2 (corta y mucho más elegante)

Con hashcat era mucho más elegante y sencillo, simplemente bastaba con ejecutar este comando y el resultado lo tenías en 6 minutos. Sólo había que tener en cuenta pasar los md5 a hexadecimal y añadir un 0 delante al md5 68cb5a1cf54c078bf0e7e89584c1a4e (temas de conversión de hex a decimal en python).

```
$ hashcat -m 0 -a 3 -1 ?d?l?u?s hashes.txt ?1?1?1?1?1
Initializing hashcat v2.00 with 2 threads and 32mb segment-size...

Added hashes from file hashes.txt: 13 (1 salts)

569f606fd6da5d612f10cfb95c0bde6d:8l6m1      
5f04850fec81a27ab5fc98befa4eb40c:5d4s2      
3122ef3a001aaecdb8dd9d843c029e06:v37j4      
c11e2cd82d1f9fbd7e4d6ee9581ff3bd:ds9v4      
068cb5a1cf54c078bf0e7e89584c1a4e:n5l67      
938c747c6a051b3e163eb802a325148e:28n4b      
adb778a0f729293e7e0b19b96a4c5a61:81h3d      
c0fd15ae2c3931bc1e140523ae934722:43s8d      
ecf8dcac7503e63a6a3667c5fb94f610:vj8nk      
1df4c637d625313720f45706a48ff20f:1n52n      
6722f7a07246c6af20662b855846c2c8:TF{dv      
831daa3c843ba8b087c895f0ed305ce7:ALEXC      
38543c5e820dd9403b57beff6020596d:6v3k}      
                                           
All hashes have been recovered

Input.Mode: Mask (?1?1?1?1?1) [5]
Index.....: 0/1 (segment), 7737809375 (words), 0 (bytes)
Recovered.: 13/13 hashes, 1/1 salts
Speed/sec.: - plains, 19.69M words
Progress..: 7449479812/7737809375 (96.27%)
Running...: 00:00:06:18
Estimated.: 00:00:00:14


Started: Sun Feb  5 21:02:41 2017
Stopped: Sun Feb  5 21:08:59 2017
```
