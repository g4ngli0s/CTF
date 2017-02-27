-----
#### Rising Research (200 pts)
#### CTF: Fwhibbit CTF 2017
#### URL: https://ctf.followthewhiterabbit.es/
#### CAT: forensics

-----

Points: 200 
Country: Thailand 

Attachment: https://mega.nz/#!I5kRCJqA!xSaCEtbljgBpOE8q6C3OmhK_Yyxe62BdiNwBBaKEM7o 

Description: An infiltrated russian spy has sent us a file that indicates the name of a Doctor of 
great relevance in the advanced projects on Artificial Intelligence (IA). According to an intelligence 
report, we should omit the place where the information leak occurred: the Massachusetts Institute of 
Technology.

-----
Hint (-75 points)

The magic numbers are very helpful as is the ASCII code of the PNG images.
There is a clue in the course of the resolution of the challenge, observing 
in the ASCII code. This steganography must be applied 

-----
## (1) ANALYSIS OF THE FILES WITH AN HEXADECIMAL EDITOR

Once decompressed, the provided attachment contains the following 25 PNG files:

```
$ ls -al *.png
-rw-r--r-- 1 sn4fu sn4fu  278335 Feb 18 17:18 20161107_odhgos_mh_sexistikhs_glwssas(2).png
-rw-r--r-- 1 sn4fu sn4fu  266969 Feb 18 17:20 20161109_logoCenter_1140x670.png
-rw-r--r-- 1 sn4fu sn4fu 1249243 Feb 18 17:14 4DO1rnQ83ny.png
-rw-r--r-- 1 sn4fu sn4fu  227173 Feb 18 17:22 blog-highlights-ellucian-wt-bogota.png
-rw-r--r-- 1 sn4fu sn4fu  386597 Feb 18 17:24 Cookies.png
-rw-r--r-- 1 sn4fu sn4fu  355155 Feb 18 17:26 Cover-18.png
-rw-r--r-- 1 sn4fu sn4fu  539250 Feb 18 17:27 Dailymotion_PS4App-DMBlue.png
-rw-r--r-- 1 sn4fu sn4fu   18224 Feb 18 17:28 default-image.png
-rw-r--r-- 1 sn4fu sn4fu  294444 Feb 18 17:29 facebook.png
-rw-r--r-- 1 sn4fu sn4fu 1304979 Feb 18 17:30 fb-og.png
-rw-r--r-- 1 sn4fu sn4fu   26640 Feb 18 17:37 freddie.png
-rw-r--r-- 1 sn4fu sn4fu   23975 Feb 18 17:39 github-mark.png
-rw-r--r-- 1 sn4fu sn4fu   40558 Feb 18 17:42 Image.png
-rw-r--r-- 1 sn4fu sn4fu  137214 Feb 18 17:45 kt_home_member-min.png
-rw-r--r-- 1 sn4fu sn4fu   11769 Feb 18 17:47 lc-og@2x.png
-rw-r--r-- 1 sn4fu sn4fu   23563 Feb 18 17:48 newTsol_logo_socmedia.png
-rw-r--r-- 1 sn4fu sn4fu   42858 Feb 18 17:49 obywatel-opengraph.png
-rw-r--r-- 1 sn4fu sn4fu  587575 Feb 18 19:10 og-image-cc.png
-rw-r--r-- 1 sn4fu sn4fu   11033 Feb 18 19:10 og-image.png
-rw-r--r-- 1 sn4fu sn4fu  794269 Feb 18 19:11 report05.png
-rw-r--r-- 1 sn4fu sn4fu   45252 Feb 18 19:21 snworks-logo-facebook.png
-rw-r--r-- 1 sn4fu sn4fu   37488 Feb 18 19:21 study-logo-og-new.png
-rw-r--r-- 1 sn4fu sn4fu  427313 Feb 18 19:22 ucal-fb-image.png
-rw-r--r-- 1 sn4fu sn4fu  136805 Feb 18 19:23 v2-frontpage-fb.png
-rw-r--r-- 1 sn4fu sn4fu  114093 Feb 18 19:23 zte-grand-s-ext.png
```

But unforrtunately we are not able to display any of them. As we can see using an hex editor, the headers seem to be corrupted because there is no trace of the PNG magic numbers before the iHDR chunk on each file. The magic numbers have been overwritten with other strings. Checking all the files in alphabetical order reveals the following:

```
20161107_odhgos_mh_sexistikhs_glwssas\(2\).png
00000000   E3 55 45 44  56 45 53 53  00 00 00 0D  49 48 44 52  00 00 04 74  00 00 02 9E  .UEDVESS....IHDR...t....

20161109_logoCenter_1140x670.png
00000000   41 51 55 49  20 45 53 54  00 00 00 0D  49 48 44 52  00 00 04 72  00 00 02 9D  AQUI EST....IHDR...r....

4DO1rnQ83ny.png
00000000   34 38 43 56  12 67 32 87  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  48CV.g2.....IHDR.......v

blog-highlights-ellucian-wt-bogota.png
00000000   45 53 54 41  20 4C 41 0A  00 00 00 0D  49 48 44 52  00 00 04 B1  00 00 02 77  ESTA LA.....IHDR.......w

Cookies.png
00000000   66 6C 61 67  7B 33 73 74  49 48 44 52  00 00 04 B0  00 00 02 76  08 06 00 00  flag{3stIHDR.......v....

Cover-18.png
00000000   34 73 5F 67  75 34 70 30  00 00 00 0D  49 48 44 52  00 00 04 38  00 00 02 D0  4s_gu4p0....IHDR...8....

Dailymotion_PS4App-DMBlue.png
00000000   5F 71 75 33  5F 33 73 74  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  _qu3_3st....IHDR.......v

default-image.png
00000000   34 5F 33 73  5F 6C 34 5F  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  4_3s_l4_....IHDR.......v

facebook.png
00000000   66 6C 34 67  5F 74 72 79  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  fl4g_try....IHDR.......v

fb-og.png
00000000   5F 68 34 72  64 33 72 7D  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  _h4rd3r}....IHDR.......v
```

If we merge all the ASCII strings at the beginning of each file, we get the following fake flag:

flag{3st4s_gu4p0_qu3_3st4_3s_l4_fl4g_try_h4rd3r}

Now we follow on with the remaining files:

```
freddie.png
00000000   5A 6E 64 6F  61 57 4A 69  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  ZndoaWJi....IHDR.......v

github-mark.png
00000000   61 58 52 37  59 6A 52 7A  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  aXR7YjRz....IHDR.......v

Image.png
00000000   4D 7A 59 30  58 32 4A 31  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  MzY0X2J1....IHDR.......v

kt_home_member-min.png
00000000   4D 32 35 66  61 57 35 30  00 00 00 0D  49 48 44 52  00 00 03 E8  00 00 03 11  M25faW50....IHDR........

lc-og@2x.png
00000000   4D 32 35 30  4D 46 39 30  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  M250MF90....IHDR.......v

newTsol_logo_socmedia.png
00000000   63 6E 6C 66  61 44 52 79  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  cnlfaDRy....IHDR.......v

obywatel-opengraph.png
00000000   5A 44 4E 79  66 51 3D 3D  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  ZDNyfQ==....IHDR.......v
```

The same procedure reveals a base64 string:

ZndoaWJiaXR7YjRzMzY0X2J1M25faW50M250MF90cnlfaDRyZDNyfQ==

Once decoded, we get a new fake flag:

```
$ echo ZndoaWJiaXR7YjRzMzY0X2J1M25faW50M250MF90cnlfaDRyZDNyfQ== | base64 --decode
fwhibbit{b4s364_bu3n_int3nt0_try_h4rd3r}
```

There are still more files which we examine using the hex editor:

```
og-image-cc.png
00000000   2E 2E 6A 67  2E 2E 67 2E  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  ..jg..g.....IHDR.......v

og-image.png
00000000   2E 2E 2E 2E  2E 67 2E 2E  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  .....g......IHDR.......v

report05.png
00000000   68 2E 2E 6E  74 2E 2E 2E  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  h..nt.......IHDR.......v

snworks-logo-facebook.png
00000000   2E 2E 2E 79  65 2E 61 68  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  ...ye.ah....IHDR.......v
``` 

The last one contains a string of interest, which we will examine later:

TWUgZW5jYW50YSBsYSBJQSwgcmZnaHF2bnFiIHJhIHBueXZzYmVhdm4==

And now the last files, which do not reveal anything interesting:
```
study-logo-og-new.png
00000000   2E 76 62 67  6E 2E 2E 2E  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  .vbgn.......IHDR.......v

ucal-fb-image.png
00000000   2E 6E 67 47  66 6E 2C 2E  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  .ngGfn,.....IHDR.......v

v2-frontpage-fb.png
00000000   2E 2E 2E 79  67 66 64 6A  00 00 00 0D  49 48 44 52  00 00 04 B0  00 00 02 76  ...ygfdj....IHDR.......v

zte-grand-s-ext.png
00000000   2E 2E 6A 2E  39 2E 35 34  00 00 00 0D  49 48 44 52  00 00 03 37  00 00 01 80  ..j.9.54....IHDR...7....
```

We decode the base64 string found in the 'snworks-logo-facebook.png' file:

```
$ echo TWUgZW5jYW50YSBsYSBJQSwgcmZnaHF2bnFiIHJhIHBueXZzYmVhdm4== | base64 --decode
Me encanta la IA, rfghqvnqb ra pnyvsbeavn
```

After some investigations, we conclude that the second part of the decoded string 'rfghqvnqb ra pnyvsbeavn' is cyphered using a simple ROT13 cypher. Decyphering it is easy:

```
$ echo "rfghqvnqb ra pnyvsbeavn" | tr '[A-Za-z]' '[N-ZA-Mn-za-m]'
estudiado en california
```
So it seems that we found a hint:
Me encanta la IA, estudiado en california


-----
## (2) REBUILDING THE PNG FILES

The next step was rebuilding the PNG files in order to be able to display them and look for more information. The magic number of a PNG file is '89 50 4e 47 0d 0a 1a 0a' and we can easily see tha its length is just the amount of bytes overwritten on each file. In order to restore the magic numbers in all the PNG files we use the following script:

```
#!/bin/bash

for file in /home/sn4fu/CTF/fwhibbit/forensics/rising_research/tmp/*
do
  printf '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' | dd conv=notrunc of=$file  bs=1
done
```
However, after the restoration process and using the 'pngcheck' tool we see that there are still 3 files with errors:

```
$ pngcheck 4DO1rnQ83ny.png 
4DO1rnQ83ny.png:  invalid chunk name "BAT#" (42 41 54 23)
ERROR: 4DO1rnQ83ny.png

$ pngcheck Cookies.png 
Cookies.png:  invalid chunk name "" (00 00 04 ffffffb0)
ERROR: Cookies.png

$ pngcheck snworks-logo-facebook.png 
snworks-logo-facebook.png  CRC error in chunk IDAT (computed 23e5ddc7, expected f1779cd6)
ERROR: snworks-logo-facebook.png
```

Examining in more detail 'Cookies.png' and comparing it with other successfully restored files, we see that it has a slightly different structure:

```
Cookies.png
00000000   89 50 4E 47  0D 0A 1A 0A  49 48 44 52  00 00 04 B0  00 00 02 76  08 06 00 00  flag{3stIHDR.......v....

Cover-18.png
00000000   89 50 4E 47  0D 0A 1A 0A  00 00 00 
```

Using the HxD hexadecimal editor in Windows, we insert the hex values '00 00 00' before '49 48 44 52'. The image is repaired but once displayed it does not reveal anything interesting.

Examining the file '4DO1rnQ83ny.png', we see that there is no iEND chunk at the end of the file. This chunk is compulsory for PNG files. The file contains the following strings at the end:

```
00130FC4   00 03 00 B4  84 8B 14 AA  EB 36 24 00  00 00 00 42  41 54 23 AE  42 60 82                  .........6$....BAT#.B`.
```
Using our hex editor, we overwrite 'BAT#' with 'IEND' and the image is repaired, but again we don't see anything of interest.

And finally, as we saw with 'pngcheck' the file 'snworks-logo-facebook.png' contains a CRC error in an iDAT chunk:
```
0000B0A4   40 08 00 00  00 00 08 D3  FF 2F C0 00  07 E0 DB 27  F1 77 9C D6  00 00 00 00  49 45 4E 44  @......../.....'.w......IEND
```

We overwrite the wrong CRC 'f1779cd6' with the expected one '23e5ddc7' and we are able to display the file. Nothing interesting.


-----
## (3) HOMING MISSILE

At this point, lots of stego tools were used against all the PNG files, to no avail. But then if we read again the hint we got from the decoded base64 string:

'Me encanta la IA, estudiado en california'

We see that there is precisely a file 'ucal-fb-image.png' that once displayed shows an University of California logo. If we zoom in the file, on the bottom left part we can see what it seems to be a part of an string. Using a contrast filter with the image reveals the following hidden hex string:
















