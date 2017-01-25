### ==================================================
### Evidencia Volátil (175pts) write-up
### CTF: CIBERSEG 2017
### URL: https://ciberseg.uah.es/ctf.html
### CAT: forensics
### ==================================================

Ups! Un ponente del ciberseg 2016 se dejo un disco duro con evidencias. Veamos si podemos conseguir alguna contraseña.

Evidencias:

https://drive.google.com/drive/folders/0BzLA9WAiAXudNEZRYTgxZkxjWWM?usp=sharing

ZIP:

-MD5: 973f998512c602bac4b8e16dbfff4575

-SHA1:4d074d765b9229df33ca473d88e85bb2bbb5341d


***

Oops! A speaker of Ciberseg 2016 forgot a hard disk with evidences. Let's see whether we can get some passwords.

Evidences:

https://drive.google.com/drive/folders/0BzLA9WAiAXudNEZRYTgxZkxjWWM?usp=sharing

ZIP:

-MD5: 973f998512c602bac4b8e16dbfff4575

-SHA1:4d074d765b9229df33ca473d88e85bb2bbb5341d

-Contains: 'ram1.mem'


***

## (1) IDENTIFICATION OF THE OS

The file contains what seems to be a RAM snapshot. First step is to try to identify the OS (Profile) of the computer where the RAM snapshot was taken:

    $ volatility -f ram1.mem imageinfo
    Volatility Foundation Volatility Framework 2.5
    INFO    : volatility.debug    : Determining profile based on KDBG search...
              Suggested Profile(s) : Win7SP1x86_BBA98F40, Win7SP0x86, Win7SP1x86
                         AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                         AS Layer2 : FileAddressSpace (/home/isma/CTF/CTF-Ciberseg-2017/forense/evidencia/ram1.mem)
                          PAE type : PAE
                               DTB : 0x185000L
                              KDBG : 0x82961c30L
              Number of Processors : 1
         Image Type (Service Pack) : 1
                    KPCR for CPU 0 : 0x82962c00L
                 KUSER_SHARED_DATA : 0xffdf0000L
               Image date and time : 2017-01-09 13:03:38 UTC+0000
         Image local date and time : 2017-01-09 05:03:38 -0800

All candidate profiles are Windows 7: Win7SP1x86_BBA98F40, Win7SP0x86, Win7SP1x86


## (2) SAM DATABASE DUMPING

In a Windows OS, the usernames and passwords are stored in the SAM database, which is loaded in memory. We can try to dump the database from the RAM snapshot:

    $ volatility hashdump --profile=Win7SP1x86_BBA98F40 -f ram1.mem 
    Volatility Foundation Volatility Framework 2.5
    Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
    IEUser:1000:aad3b435b51404eeaad3b435b51404ee:ea0026d2bc07d7f56ea8e3599cabed43:::

Dumped hashes:

    31d6cfe0d16ae931b73c59d7e0c089c0
    ea0026d2bc07d7f56ea8e3599cabed43


## (3) CRACKING HASHES WITH MIMIKATZ

We will use 'mimikatz' as a 'volatility' plugin to crack the hashes. The procedure to install 'mimikatz' as a plugin is:

    # cd /usr/share/volatility/
    # mkdir plugins
    # cd plugins 
    # wget https://raw.githubusercontent.com/dfirfpi/hotoloti/master/volatility/mimikatz.py
    # pip install construct
    # apt-get install python-crypto

Checking whether the plugin is operative:

    # ./vol.py --plugins=./plugins/ --info | grep mimikatz
    Volatility Foundation Volatility Framework 2.5
    mimikatz                   - mimikatz offline

Using the plugin with the forensic image:

    # volatility --plugins=/usr/share/volatility/plugins --profile=Win7SP0x86 -f ram1.mem mimikatz
    Volatility Foundation Volatility Framework 2.5
    Module   User             Domain           Password                                
    -------- ---------------- ---------------- ----------------------------------------
    wdigest  IEUser           IE8Win7          flag{cadia}                             
    wdigest  IE8WIN7$         WORKGROUP                          

The resulting flag is:

    flag{cadia}

