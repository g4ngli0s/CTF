### ========================================
### CR2: Many time secrets (100 pts)
### CTF: AlexCTF 2017
### URL: https://ctf.oddcoder.com/
### CAT: crypto
### ========================================

This time Fady learned from his old mistake and decided to use onetime pad as his encryption
technique, but he never knew why people call it one time pad!
```
0529242a631234122d2b36697f13272c207f2021283a6b0c7908
2f28202a302029142c653f3c7f2a2636273e3f2d653e25217908
322921780c3a235b3c2c3f207f372e21733a3a2b37263b313012
2f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d
283f652c2b31661426292b653a292c372a2f20212a316b283c09
29232178373c270f682c216532263b2d3632353c2c3c2a293504
613c37373531285b3c2a72273a67212a277f373a243c20203d5d
243a202a633d205b3c2d3765342236653a2c7423202f3f652a18
2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c
263e203d63232f0f20653f207f332065262c3168313722367918
2f2f372133202f142665212637222220733e383f2426386b
```

It seems that there are 11 ciphertexts which have been cyphered using the same One-Time Pad (OTP).

A known attack in this kind of scenario is the 'Many Time Pad Attack' described here:

###Many Time Pad Attack - Crib Drag

http://travisdazell.blogspot.com.es/2012/11/many-time-pad-attack-crib-drag.html

The phases of the attack are:

1 Guess a word that might appear in one of the messages
2 Encode the word from step 1 to a hex string
3 XOR the two cipher-text messages
4 XOR the hex string from step 2 at each position of the XOR of the two cipher-texts (from step 3)
5 When the result from step 4 is readable text, we guess the English word and expand our crib search.
6 If the result is not readable text, we try an XOR of the crib word at the next position.

There is an implementation of this attack using Python:

https://github.com/Jwomers/many-time-pad-attack/blob/master/attack.py

According to the author:

" This code investigates the properties of the one time pad - specifically that it can easily be broken if the same key is used more than once!
Given 10 ciphertexts encrypted using the same key, we can break the encryption, and generate all the plaintexts"

We just modify the script so the strings c[1..10] are initialized with our own 10 first ciphertexts.

Besides that, we configure an additional line at the end of ths script in order to print the reversed OTP key ('final_key_hex'):

```
print final_key_hex
```

We execute the script:

```
# ./script.py 
ncry*tion*s**e*e *lwa*s.
414c45580054467b48005200004700455300544845004b45007d00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
```

So the computed OTP key in hex format is:

```
414c45580054467b48005200004700455300544845004b45007d
```

Upon converting the hex string to ASCII, we get:

```
ALEX[0]TF{H[0]R[0][0]G[0]ES[0]THE[0]KE[0]}
```

So we can infer that the flag is:

```
ALEXCTF{HERE_GOES_THE_KEY}
```





