### ==================================================
### Web II write-up
### CTF: CIBERSEG 2017
### URL: https://ciberseg.uah.es/ctf.html
### CAT: web
### ==================================================

En este reto hemos hecho una página especial para aquellos que usen un sistema operativo diferente.

http://retos.ciberseg.uah.es/retos/web2.php

O en:

http://yuki.ddom.me/retos/web2.php


***

For this challenge, we have created a special web site for those who use a different operatig system:

http://retos.ciberseg.uah.es/retos/web2.php

Or:

http://yuki.ddom.me/retos/web2.php

***

We try to download the main file of the site:

http://retos.ciberseg.uah.es/retos/web2.php

    # wget http://retos.ciberseg.uah.es/retos/web2.php

The contents of the file are:

    # cat web2.php

   <html>
   No estás entrando desde: <br><img src="https://linuxerofurioso.files.wordpress.com/2015/10/haiku-logo.png"/> <br></html>


Translation: You are not accesing from https://linuxerofurioso.files.wordpress.com/2015/10/haiku-logo.png.

Haiku is a Linux distro which includes its own browser called 'WebPositive'. We perform a google search for the User Agent of this browser and we include it in the header of our request:


    # wget --user-agent="Mozilla/5.0 (compatible; U; InfiNet 0.1; Haiku) AppleWebKit/528+ (KHTML, like Gecko) WebPositive/528+ Safari/528+" http://retos.ciberseg.uah.es/retos/web2.php

This time we are able to get the flag:

    # cat web2.php 
    <html>
    flag{f1e19dad9c749f4baa77c2675b68027e}</html>
