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

'''
# tshark -r fore2.pcap -Y 'usb.capdata and usb.device_address==3' -T fields -e usb.capdata > raw
'''
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













