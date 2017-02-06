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
## (1) PRELIMINARY ANALYSIS WITH WIRESHARK

We open the pcap file with Wireshark and quickly see that it is the capture of several USB data transfers between a host and what seems to be an USB flash drive. The filters that can be used in Wireshark for this kind of traffic are described here:

https://www.wireshark.org/docs/dfref/u/usb.html

It looks like the interesting data has been transferred in packets of the USB protocol described as 'URB_BULK out' because there are interesting strings inside them and they are the ones with larger size, due to the fact that they correspond to USB messages of the type 'bulk transfer', used for bulk data transfers.

On the other hand, we see that this bulk data is transferred to a device with address '3' in the USB bus, so we build the following Wireshark filter to get those packets only:

usb.device_address==3 && usb.capdata

More precisely, the interesting data is stored in the field 'Leftover Capture Data', so we righ-click on it and select 'Apply as Column' so we can see it in the main Wireshark window.





