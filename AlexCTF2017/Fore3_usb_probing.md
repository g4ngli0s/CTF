### =============================================
### Fore3: USB probing (150 pts)
### CTF: AlexCTF 2017
### URL: https://ctf.oddcoder.com/
### CAT: forensics
### =============================================

One of our agents managed to sniff important piece of data transferred transmitted via USB, he told
us that this pcap file contains all what we need to recover the data can you find it ?

fore2.pcap

-------------------------------------------------
## (1) PRELIMINARY ANALYSIS (wireshark)

We open the pcap file with Wireshark and quickly see that it is the capture of several USB data transfers between a host and what seems to be an USB flash drive. The filters that can be used in Wireshark for this kind of traffic are described here:

https://www.wireshark.org/docs/dfref/u/usb.html

It looks like the interesting data has been transferred in packets of the USB protocol described as 'URB_BULK out' because there are interesting strings inside them and they are the ones with larger size, due to the fact that they correspond to USB messages of the type 'bulk transfer', used for bulk data transfers.

On the other hand, we see that this bulk data is transferred to a device with address '3' in the USB bus, so we build the following Wireshark filter to get those packets only:

usb.device_address==3 && usb.capdata

More precisely, the interesting data is stored in the field 'Leftover Capture Data', so we righ-click on it and select 'Apply as Column' so we can see it in the main Wireshark window.

-------------------------------------------------
## (2) PACKET FILTERING (tshark)

We can perform the same filtering using 'tshark' from the command line, which may be useful in order to extract the packets later:

```
$ tshark -r fore2.pcap -Y 'usb.capdata and usb.device_address==3' -T text
 39  16.098585         host -> 3.3.2        USB 24640 c03b39980000000100000095000004250000000000000000... 0xffff8fbdab26acc0 URB_BULK out
 49  17.210219         host -> 3.3.2        USB 4160 c03b39980000000200000095000000000000000000000000... 0xffff8fbe0802f900 URB_BULK out
 63  22.300886         host -> 3.3.2        USB 8256 c03b39980000000100000096000004260000000800000000... 0xffff8fbdab3fd780 URB_BULK out
 69  22.302398         host -> 3.3.2        USB 4160 c03b39980000000200000096000000000000000000000000... 0xffff8fbdab3fd780 URB_BULK out
 83  26.396865         host -> 3.3.2        USB 4160 ffffff030000000000000000000000000000000000000000... 0xffff8fbcea2b4780 URB_BULK out
 89  26.399860         host -> 3.3.2        USB 4160 00000000000000001a5665581a5665581a56655800000000... 0xffff8fbcea2b4780 URB_BULK out
 95  26.401307         host -> 3.3.2        USB 4160 020000000c0001022e000000020000000c0002022e2e0000... 0xffff8fbcea2b4780 URB_BULK out
101  26.404412         host -> 3.3.2        USB 61504 89504e470d0a1a0a0000000d49484452000001cc00000082... 0xffff8fbdab26acc0 URB_BULK out
119  32.028809         host -> 3.3.2        USB 16448 c03b39980000000100000097000004060000000000000000... 0xffff8fbda7491180 URB_BULK out
125  32.031301         host -> 3.3.2        USB 4160 c03b39980000000200000097000000000000000000000000... 0xffff8fbdab26af00 URB_BULK out
```

-------------------------------------------------
## (3) PACKET EXTRACTION IN HEX FORMAT (tshark)

We proceed to extract the packets using the same filter:

```
# tshark -r fore2.pcap -Y 'usb.capdata and usb.device_address==3' -T fields -e usb.capdata > raw
```

Options used:

-r: Read packet data from infile.

-Y: Display filter (same we used in section 2).

-T: Set the format of the output when viewing decoded packet data ('fields' format).

-e: <field> Add a field to the list of fields to display if -T fields is selected.

usb.capdata -> get packet data from the 'USB Leftover' field one, which is the one we are interested in.

Al the extracted packets are stored in the 'raw' file, one packet on each line. In order to merge all the packets in a unique string, we edit the file and merge the lines, paying attention to append ':' between each two lines, so the hex format is not broken. This operation can be performed using any decent text editor such Notepad++.

Just in case we need to analize an isolated packet, we coud use the following tshark filter (i.e. for packet 101):
```
# tshark -r fore2.pcap -Y 'usb.capdata and usb.device_address==3 and frame.number==101' -T fields -e usb.capdata > raw101
```

-------------------------------------------------
## (4) HEX TO BIN CONVERSION (xxd)

Now we convert our hex file to binary using 'xxd':

```
# xxd -r -p raw_agrupado output2.bin
```

Options used:

-r: revert - reverse operation: convert (or patch) hexdump into binary

-p: plain hexdump style


-------------------------------------------------
## (5) STRINGS SEARCH (strings)

We can use 'strings' to look for interesting strings in our new binary:

```
$ strings output2.bin | more
/....................../
ICst
.Trash-1000
Cryptoe6
Hardware
Vulnerability Research
Developmentn
Reverse Engineeringo
Flag.mp4
Forensics.mp
The Heap - Once upon a free().mp4sploit-like_tool_for_hardware_hacking_hd.mp4amm
28c3-4735-en-reverse_engineering_a_qualcomm_baseband.webm
30c3-5477-en-An_introduction_to_Firmware_Analysis_h264-hd.mp4
reverse engineering a qualcomm baseband.webm
/....................../
```

We find an interesting string named 'Flag.mp4', although as we'll see later, it is a fake flag.

-------------------------------------------------
## (6) FILE CARVING (binwalk)

We use 'binwalk' to perform file carving on the binary, looking for hidden files inside it:

```
$ binwalk -Me output2.bin 

Scan Time:     2017-02-04 17:35:10
Target File:   /home/isma/CTF/alexCTF17/forensics/fore3/output2.bin
MD5 Checksum:  6c35fb1fe9e1cbde5618db7b2f3a9037
Signatures:    344

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
53248         0xD000          PNG image, 460 x 130, 8-bit/color RGBA, interlaced
```

Binwalk finds a hideen PNG image inside the binary. If it is not extracted with the previous command, we can force it using:

```
$ binwalk -D 'png image:png' output2.bin 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
53248         0xD000          PNG image, 460 x 130, 8-bit/color RGBA, interlaced
```

The image is stored in the '_output2.bin.extracted/' filder. Displaying the image we get the flag:

ALEXCTF{SN1FF_TH3_FL4G_OV3R_USB}

Important note: the Linux 'display' command is unable to open the PNG, stating that it is a corrupted file. However, it can be smoothly opened from W10.

Final note: in the carving process we used three more tools, to no avail:

- FOREMOST:

```
$ foremost -v -i output2.bin
Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus
Audit File

Foremost started at Sat Feb  4 17:51:07 2017
Invocation: foremost -v -i output2.bin 
Output directory: /home/isma/CTF/alexCTF17/forensics/fore3/output
Configuration file: /etc/foremost.conf
Processing: output2.bin
|------------------------------------------------------------------
File: output2.bin
Start: Sat Feb  4 17:51:07 2017
Length: 132 KB (135168 bytes)
 
Num	 Name (bs=512)	       Size	 File Offset	 Comment 

*|
Finish: Sat Feb  4 17:51:07 2017

0 FILES EXTRACTED
	
------------------------------------------------------------------

Foremost finished at Sat Feb  4 17:51:07 2017
```

- SCALPEL:

```
$ scalpel -c scalpel_cfg.conf -o output_scalpel/ output2.bin

$ cat audit.txt 

Scalpel version 1.60 audit file
Started at Sat Feb  4 17:51:43 2017
Command line:
scalpel -c scalpel_cfg.conf -o output_scalpel/ output2.bin 

Output directory: /home/isma/CTF/alexCTF17/forensics/fore3/output_scalpel
Configuration file: scalpel_cfg.conf

Opening target "/home/isma/CTF/alexCTF17/forensics/fore3/output2.bin"

The following files were carved:
File		  Start			Chop		Length		Extracted From
00000007.pgp        77563		YES           57606		output2.bin
00000006.pgp        24587		YES          100000		output2.bin
00000005.pgp           11		YES          100000		output2.bin
00000004.pgp       102129		YES           33040		output2.bin
00000003.pgp        65541		YES           69628		output2.bin
00000002.pgp        55579		YES           79590		output2.bin
00000001.mov        49383		YES           85786		output2.bin
00000000.mov        20711		YES          114458		output2.bin


Completed at Sat Feb  4 17:51:43 2017
```

Note: 'scalpel_cfg.conf' is a copy of '/etc/scalpel/scalpel.conf' modified so all the file types are uncommented and file carving is performed using all of them.

- BULK EXTRACTOR:

```
$ bulk_extractor -o output/ output.bin
bulk_extractor version: 1.6.0-dev
Hostname: cathedral
Input file: output.bin
Output directory: output/
Disk Size: 86016
Threads: 2
Attempt to open output.bin
All data are read; waiting for threads to finish...
Time elapsed waiting for 1 thread to finish:
    1 sec (timeout in 59 min59 sec.)
All Threads Finished!
Producer time spent waiting: 0 sec.
Average consumer time spent waiting: 0.0524705 sec.
MD5 of Disk Image: 02f8510a63063bde004845ac0f30ca17
Phase 2. Shutting down scanners
Phase 3. Creating Histograms
Elapsed time: 0.121984 sec.
Total MB processed: 0
Overall performance: 0.705142 MBytes/sec (0.352571 MBytes/sec/thread)
Total email features found: 0
```











