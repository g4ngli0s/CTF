### ==================================================
### Crypto II (20pts) write-up
### CTF: CIBERSEG 2017
### URL: https://ciberseg.uah.es/ctf.html
### CAT: crypto
### ==================================================

Una de hashes en formato password de la UAH:

    a522c8bf85a95c066bb2a8a85309c5c431652342
    1e230c2310c38677c2d1f9bf358539616f2fd89a
    c2b7df6201fdd3362399091f0a29550df3505b6a

Para los no alumnos de la UAH:
El formato de las contraseñas de la UAH es: 3 minúsculas, 1 carácter especial y 4 números.

Nota: el formato de la bandera es 'flag{}'

***

In this challenge, the following hashed passwords from the UAH are provided:

    a522c8bf85a95c066bb2a8a85309c5c431652342
    1e230c2310c38677c2d1f9bf358539616f2fd89a
    c2b7df6201fdd3362399091f0a29550df3505b6a

Hint: format of the passwords is: 3 lowercase, 1 special character, 4 numbers.

Note: flag format is flag{}

***

## (1) HASH IDENTIFICATION

First step is try to identify the hash type. We can use the 'hash-identifier' tool, included in Kali:

    $ hash-identifier
       #########################################################################
       #	 __  __ 		    __		 ______    _____	   #
       #	/\ \/\ \		   /\ \ 	/\__  _\  /\  _ `\	   #
       #	\ \ \_\ \     __      ____ \ \ \___	\/_/\ \/  \ \ \/\ \	   #
       #	 \ \  _  \  /'__`\   / ,__\ \ \  _ `\	   \ \ \   \ \ \ \ \	   #
       #	  \ \ \ \ \/\ \_\ \_/\__, `\ \ \ \ \ \	    \_\ \__ \ \ \_\ \	   #
       #	   \ \_\ \_\ \___ \_\/\____/  \ \_\ \_\     /\_____\ \ \____/	   #
       #	    \/_/\/_/\/__/\/_/\/___/    \/_/\/_/     \/_____/  \/___/  v1.1 #
       #								 By Zion3R #
       #							www.Blackploit.com #
       #						       Root@Blackploit.com #
       #########################################################################
    
       -------------------------------------------------------------------------
     HASH: 1e230c2310c38677c2d1f9bf358539616f2fd89a

    Possible Hashs:
    [+]  SHA-1
    [+]  MySQL5 - SHA-1(SHA-1($pass))

    Least Possible Hashs:
    [+]  Tiger-160
    [+]  Haval-160
    /....../

We get the same result for the 3 hashes.


## (2) BRUTEFORCE ATTACK TO THE SECOND HASH USING HASHCAT

We start a bruteforce attack against the second hash, using the 'hashcat' tool included in Kali and specifying 'SHA1' as hashing algorithm:

    # hashcat -m 100 -a3 hashes.txt ?l?l?l?s?d?d?d?d
    
    1e230c2310c38677c2d1f9bf358539616f2fd89a:uah#5674
    
    Input.Mode: Mask (?l?l?l?s?d?d?d?d) [8]
    Index.....: 0/1 (segment), 5800080000 (words), 0 (bytes)
    Recovered.: 1/3 hashes, 0/1 salts
    Speed/sec.: 14.51M plains, 14.51M words
    Progress..: 5800080000/5800080000 (100.00%)
    Running...: 00:00:06:40
    Estimated.: --:--:--:--
    
    Started: Sat Jan 21 01:13:54 2017            
    Stopped: Sat Jan 21 01:20:35 2017

Parameters used:

-m 100: SHA1 algorithm (see https://hashcat.net/wiki/doku.php?id=example_hashes)

-a3: bruteforce attack (a mask is specified, so it is a mask attack instead)

?l?l?l?s?d?d?d?d: mask (see https://hashcat.net/wiki/doku.php?id=mask_attack)

hashes.txt: file containing the hashes.

Results:

1e230c2310c38677c2d1f9bf358539616f2fd89a:uah#5674


We try the same attack to the other two hashes, using other candidate algorithms, to no avail:

Double SHA1:

    # hashcat -m 4500 -a3 hashes.txt ?l?l?l?s?d?d?d?d

sha1(sha1(sha1($pass)))

    # hashcat -m 4600 -a3 hashes.txt ?l?l?l?s?d?d?d?d

sha1(md5($pass))

    # hashcat -m 4700 -a3 hashes.txt ?l?l?l?s?d?d?d?d

MySQL4.1/MySQL5+

    # hashcat -m 300 -a3 hashes.txt ?l?l?l?s?d?d?d?d

We also try permutations using our own custom charsets:

    # hashcat -m 100 -a 3 -1 ?l?l?l?s?d?d?d?d hashes.txt ?1?1?1?1?1?1?1?1

Other combinations:

LLLSDDDD
DDDDSLLL
SLLLDDDD
SDLLLDDD
SDDLLLDD
SDDDLLLD
DLLLSDDD
DDLLLSDD
DDDLLLSD
DDDDLLLS
LLLDDDDS
LLLDDDSD
LLLDDSDD
LLLDSDDD

In the end this approach is too complex and time consuming.



## (3) PARTIAL KNOWN PLAINTEXT ATTACK TO THE FIRST HASH

We take advantage of the fact that we know that all flags start with the string 'flag{' to attack the first hash:

    # hashcat -m 100 -a 3 hash1.txt flag{
    Initializing hashcat v2.00 with 2 threads and 32mb segment-size...
    
    Added hashes from file hash1.txt: 1 (1 salts)
    Activating quick-digest mode for single-hash
    
    a522c8bf85a95c066bb2a8a85309c5c431652342:flag{
                                                 
    All hashes have been recovered
    
    Input.Mode: Mask (flag{) [5]
    Index.....: 0/1 (segment), 1 (words), 0 (bytes)
    Recovered.: 1/1 hashes, 1/1 salts
    Speed/sec.: - plains, - words
    Progress..: 1/1 (100.00%)
    Running...: --:--:--:--
    Estimated.: --:--:--:--
    
    Started: Sat Jan 21 12:43:14 2017
    Stopped: Sat Jan 21 12:43:14 2017

Results:

a522c8bf85a95c066bb2a8a85309c5c431652342:flag{


## (4) RAINBOW TABLES ATTACK TO THE THIRD HASH

The last character of the last password must be '}' in order to accomplish with the flag format. We don't know whether there are more characters or not, but it is worth trying a Rainbow Tables attack considering the case of only a '}'. Using this online tool:

https://hashkiller.co.uk/md5-decrypter.aspx

We get the following result:

c2b7df6201fdd3362399091f0a29550df3505b6a SHA1 : }


***

The flag is:

    flag{uah#5674}
