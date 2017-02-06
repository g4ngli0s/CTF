# ===================================================================================================
# CR2: Many time secrets (100 pts)
# CTF: AlexCTF 2017
# URL: https://ctf.oddcoder.com/
# CAT: crypto
# ===================================================================================================

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

Many Time Pad Attack - Crib Drag
http://travisdazell.blogspot.com.es/2012/11/many-time-pad-attack-crib-drag.html