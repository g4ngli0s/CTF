### =================================================
### SC1: Math bot (100 pts)
### CTF: AlexCTF 2017
### URL: https://ctf.oddcoder.com/
### CAT: scripting
### =================================================

It is well known that computers can do tedious math faster than human.

nc 195.154.53.62 1337

Update
we got another mirror here

nc 195.154.53.62 7331

---------------------------------------------
# (1) RECONNAISSANCE

We use netcat to connect to the server and we get a program asking for mathematical operations:

```
$ nc 195.154.53.62 1337
                __________
         ______/ ________ \______
       _/      ____________      \_
     _/____________    ____________\_
    /  ___________ \  / ___________  \
   /  /XXXXXXXXXXX\ \/ /XXXXXXXXXXX\  \
  /  /############/    \############\  \
  |  \XXXXXXXXXXX/ _  _ \XXXXXXXXXXX/  |
__|\_____   ___   //  \\   ___   _____/|__
[_       \     \  X    X  /     /       _]
__|     \ \                    / /     |__
[____  \ \ \   ____________   / / /  ____]
     \  \ \ \/||.||.||.||.||\/ / /  /
      \_ \ \  ||.||.||.||.||  / / _/
        \ \   ||.||.||.||.||   / /
         \_   ||_||_||_||_||   _/
           \     ........     /
            \________________/

Our system system has detected human traffic from your IP!
Please prove you are a bot
Question  1 :
162309098294273405352945897941517 * 217222686798544069525763515426429 =
35257218423331055402099932577456988579653074090487608665558152793
Question  2 :
242476026148397688499487837252676 - 233856079758026898890320738162524 =
8619946390370789609167099090152
Question  3 :
170752279048800230432510921459145 * 134783211204161713863317845804244 =
3
See, you are a human...
Freeze!
```

We can use the 'bc' calculator to compute the answers and paste them manually:

```
$ bc <<< '162309098294273405352945897941517 * 217222686798544069525763515426429'
35257218423331055402099932577456988579653074090487608665558152793

$ bc <<< '242476026148397688499487837252676 - 233856079758026898890320738162524'
8619946390370789609167099090152
```

But the program continues to send questions. It looks like it is necessary to send the answers very quickly, so we can use a script able to get the mathematical operation and send the result automatically.

In case of an incorrect answer, the server closes the connection.

---------------------------------------------
# (2) ATTACK

We use the script to attack the server.





