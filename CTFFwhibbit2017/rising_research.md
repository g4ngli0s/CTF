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

fwhibbit{b4s364_bu3n_int3nt0_try_h4rd3r}













