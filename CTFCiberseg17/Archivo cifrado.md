### =================================================
### Archivo Cifrado (200pts) write-up
### CTF: CIBERSEG 2017
### URL: https://ciberseg.uah.es/ctf.html
### CAT: forensics
### =================================================

Hemos encontrado un USB con un archivo bastante raro. Antes de extraer el USB hemos tomado una captura de ram por si acaso.

Evidencias:
https://drive.google.com/drive/folders/0BzLA9WAiAXudZ0RFTzN0MnB4bG8?usp=sharing

My Documents:

-MD5: 65bb2505417afe5bb9bec183b997f9f2

-SHA-1: b6e4220de569b392434893a2e85d369c10e08091

Ram.rar:

-MD5: 7026d79a7a84531ed1459e7d1dbcf30d

-SHA-1: 82e3171e30db0a7137dc1a8aa457350b484a2bff


***

We have found an USB flash drive with a quite weird file. Before unplugging the drive, we have taken a snapshot of the RAM, just in case.

Evidences:

https://drive.google.com/drive/folders/0BzLA9WAiAXudZ0RFTzN0MnB4bG8?usp=sharing

My Documents:

-MD5: 65bb2505417afe5bb9bec183b997f9f2

-SHA-1: b6e4220de569b392434893a2e85d369c10e08091

Ram.rar:

-MD5: 7026d79a7a84531ed1459e7d1dbcf30d

-SHA-1: 82e3171e30db0a7137dc1a8aa457350b484a2bff

-Contains 'Reto2Forense.mem'.


***

## (1) IDENTIFICATION OF THE OS

First step is to try to identify the OS (Profile) of the computer where the RAM snapshot was taken:

    $ volatility -f Reto2Forense.mem imageinfo
    Volatility Foundation Volatility Framework 2.5
    INFO    : volatility.debug    : Determining profile based on KDBG search...
              Suggested Profile(s) : Win10x64_1AC738FB, Win10x64, Win10x64_DD08DD42
                         AS Layer1 : Win10AMD64PagedMemory (Kernel AS)
                         AS Layer2 : FileAddressSpace (/home/isma/CTF/CTF-Ciberseg-2017/forense/cifrado/Reto2Forense.mem)
                          PAE type : No PAE
                               DTB : 0x1aa000L
                               KDBG : 0xf80393504500L
              Number of Processors : 1
         Image Type (Service Pack) : 0
                    KPCR for CPU 0 : 0xfffff80393556000L
                 KUSER_SHARED_DATA : 0xfffff78000000000L
               Image date and time : 2017-01-09 15:59:12 UTC+0000
         Image local date and time : 2017-01-09 07:59:12 -0800

Candidates are all Windows 10: Win10x64_1AC738FB, Win10x64, Win10x64_DD08DD42


## (2) ANALYSIS OF PROCESSES RUNNING IN THE COMPUTER

It may be interesting to see which processes were running in the machine during the snapshot:

    $ volatility pslist --profile=Win10x64_1AC738FB -f Reto2Forense.mem 
    Volatility Foundation Volatility Framework 2.5
    Offset(V)          Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
    ------------------ -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
    0xffffba81aa02d480 System                    4      0    106        0 ------      0 2017-01-10 00:56:11 UTC+0000                                 
    0xffffba81ab589680 smss.exe                276      4      4        0 ------      0 2017-01-10 00:56:11 UTC+0000                                 
    0xffffba81abfeb080 csrss.exe               360    352     10        0      0      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ab792080 smss.exe                416    276      0 --------      1      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ac0e9080 wininit.exe             424    352      4        0      0      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ac14c080 csrss.exe               436    416     11        0      1      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ac18e080 winlogon.exe            492    416      6        0      1      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ac1ac700 services.exe            516    424     16        0      0      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ac1ab280 lsass.exe               524    424     10        0      0      0 2017-01-10 00:56:15 UTC+0000                                 
    0xffffba81ac4bc5c0 svchost.exe             612    516     29        0      0      0 2017-01-10 00:56:16 UTC+0000                                 
    0xffffba81ac56b6c0 svchost.exe             668    516     13        0      0      0 2017-01-10 00:56:16 UTC+0000                                 
    0xffffba81ab79c800 dwm.exe                 768    492     12        0      1      0 2017-01-10 00:56:16 UTC+0000                                 
    0xffffba81ac61f340 svchost.exe             848    516     66        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81ac55d800 svchost.exe             856    516     25        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81ac55b800 svchost.exe             884    516     21        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81ac555800 svchost.exe             908    516     18        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81aa10b180 svchost.exe             324    516     29        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81aa0af380 svchost.exe             680    516     21        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81ac4f4800 VBoxService.ex          928    516     11        0      0      0 2017-01-10 00:56:17 UTC+0000                                 
    0xffffba81ac54f800 svchost.exe            1120    516      6        0      0      0 2017-01-09 15:57:00 UTC+0000                                 
    0xffffba81ac2eb800 svchost.exe            1244    516     10        0      0      0 2017-01-09 15:57:00 UTC+0000                                 
    0xffffba81ac015080 SearchIndexer.         1336    516     14        0      0      0 2017-01-09 15:57:01 UTC+0000                                 
    0xffffba81ac334800 spoolsv.exe            1404    516     12        0      0      0 2017-01-09 15:57:01 UTC+0000                                 
    0xffffba81ac0bd800                          0   9965 42...1 -------- ------      0                          	 

No interesting processes have been identified.


## (3) TRUECRYPT APPROACH

The 'MyDocuments' file seems to be an encrypted file, so it is worth to try to see whether 'TrueCrypt' was being used:


    $ volatility truecryptsummary --profile=Win10x64_1AC738FB -f Reto2Forense.mem 
    Volatility Foundation Volatility Framework 2.5
    Password             GetRektTruecrypt7.0 at offset 0xfffff804b15ebe64
    Kernel Module        truecrypt.sys at 0xfffff804b15b0000 - 0xfffff804b15f1000
    Symbolic Link        Volume{939efd87-d6c7-11e6-b8f2-080027ccbeaf} -> \Device\TrueCryptVolumeD mounted 2017-01-09    15:58:54 UTC+0000


We confirm that the TrueCrypt passphrase was cached in memory:

    $ volatility truecryptpassphrase --profile=Win10x64_1AC738FB -f Reto2Forense.mem 
    Volatility Foundation Volatility Framework 2.5
    Found at 0xfffff804b15ebe64 length 19: GetRektTruecrypt7.0


## (4) USING TRUECRYPT TO DECRYPT THE FILE

We install TrueCrypt in a Windows machine to decypher the file:

http://truecrypt.sourceforge.net/

Once executed, in the main window right-click on a free drive and choose 'Select File and Mount...' and the encrypted file 'MyDocuments'.

Password: GetRektTruecrypt7.0

After mounting the drive, right-click in the name of the volume and select 'Open' to get a file explorer. There we can see a file named 'TextoSeguro.txt' which contains the flag:

    flag{useVeracrypt}
