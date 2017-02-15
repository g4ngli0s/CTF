## ===================================================
## dnscap (500 pts)
## CTF: BSidesSF 2017 CTF
## URL: https://scoreboard.ctf.bsidessf.com/
## CAT: forensics
## ===================================================

Found this packet capture. Pretty sure there's a flag in here. Can you find it!?

dnscap.pcap

----------
## (1) ANALYSIS OF THE PCAP FILE USING Wireshark

On this challenge, a pcap file named 'dnscap.pcap' is presented for analysis. We open it with Wireshark and see that there are lots of DNS queries and responses of the following types: CNAME, TXT and MX. On each of them, the contents of both the queries and the responses contain large hex strings.

We can use the following Wireshark filters to isolate each query/response of interest:

TXT QUERIES:
(dns.qry.type == 16) and not (dns.txt)

TXT RESPONSES:
dns.txt

MX QUERIES:
(dns.qry.type == 15) and not (dns.mx.mail_exchange)

MX RESPONSES:
dns.mx.mail_exchange

CNAME QUERIES:
(dns.qry.type == 5) and not (dns.cname)

CNAME RESPONSES:
dns.cname

Using tshark, we can extract all those packets in separated files:

TXT QUERIES
```
# tshark -r dnscap.pcap -Y '(dns.qry.type == 16) and not (dns.txt)' -T fields -e frame.number -e dns.qry.name > queries_TXT.txt
```

TXT RESPONSES
```
# tshark -r dnscap.pcap -Y 'dns.txt' -T fields -e frame.number -e dns.txt > responses_TXT.txt
```

MX QUERIES
```
# tshark -r dnscap.pcap -Y '(dns.qry.type == 15) and not (dns.mx.mail_exchange)' -T fields -e frame.number -e dns.qry.name > queries_MX.txt
```

MX RESPONSES
```
# tshark -r dnscap.pcap -Y 'dns.mx.mail_exchange' -T fields -e frame.number -e dns.mx.mail_exchange > responses_MX.txt
```

CNAME QUERIES
```
# tshark -r dnscap.pcap -Y '(dns.qry.type == 5) and not (dns.cname)' -T fields -e frame.number -e dns.qry.name > queries_CNAME.txt
```

CNAME RESPONSES
```
# tshark -r dnscap.pcap -Y 'dns.cname' -T fields -e frame.number -e dns.cname > responses_CNAME.txt
```

Note that for each capture we include the frame number, just in case it is necessary for any purpose.

Then we merge all the files in a single one:
```
# cat queries_CNAME.txt queries_MX.txt queries_TXT.txt responses_CNAME.txt responses_MX.txt responses_TXT.txt > fusion.txt
```

And generate a new merged file with all the packets ordered by frame number (first column in the file):
```
# sort -k1n,3 fusion.txt > fusion_ordenado.txt
```

Here is how this new file looks like:
```
1       05e100a621c3620001636f6e736f6c65202873697276696d65732900.skullseclabs.org
2       958700a621c3620001636f6e736f6c65202873697276696d65732900.skullseclabs.org
3       634f00a621010a0000.skullseclabs.org
4       7cd501a621c362010a.skullseclabs.org
5       96b201a621010ac362
6       b11c01a621c362010a.skullseclabs.org
7       e14001a621010ac362
8       0ab801a621c362010a.skullseclabs.org
9       0e3d01a621010ac362.skullseclabs.org
10      772301a621c362010a.skullseclabs.org
11      d01b01a621010ac362.skullseclabs.org
12      b73f01a621c362010a57656c636f6d6520746f20646e7363617021205468.6520666c61672069732062656c6f772c20686176652066756e21210a.skullseclabs.org
13      aeb101a621010ac393.skullseclabs.org
/....../
```
------
## (2) ANALYSIS OF THE CAPTURED DATA

In order to analyze the data we have just extracted, we use the following Perl script named 'bsidessf17_dnscap_script1.pl' (yeah, there is life beyond Python!):

```
#!/usr/bin/perl
#
# bsidessf17 - dnscap
#
# script de analisis inicial
#
# fusion_ordenado.txt tiene el formato: <paquete>\t<datos>
#
# Rev.20170212 by sn4fu

use strict;
use warnings;
use 5.016;

my $fichero = 'fusion_ordenado.txt';
open(my $fh,$fichero)
or die "No se ha encontrado el fichero '$fichero' $!";

while (my $linea = <$fh>) {
 chomp $linea;                                          # quitar CR
 my ($paquete, $datos) = split /\t/, $linea;            # parsear usando TAB como separador
 print "$paquete\n";                                    # imprimir numero de paquete
 print "$datos\n";                                      # imprimir datos del paquete
 my @cadenas = split /\./, $datos;                      # parsear las partes de la cadena de datos separadas con '.'
 my $cadena_sobrante1 = 'org';                          # las cadenas 'org' no nos interesan
 @cadenas = grep {!/$cadena_sobrante1/} @cadenas;
 my $cadena_sobrante2 = 'skullseclabs';                 # las cadenas 'skullseclabs' no no sinteresan
 @cadenas = grep {!/$cadena_sobrante2/} @cadenas;
 foreach (@cadenas)
   {
      print "$_\n";                                     # imprimir la cadena HEX
      say (pack "H*",$_);                               # traducir la cadena a ASCII
   }
}
```
This script reads each line (packet) of the file, parses the frame number and the payload and parses the payload as well in order to extract the strings separated by '.'. Then it deletes all the strings 'org' and 'skullseclabs' (we are interested just in the hex strings) and converts the hex strings to ASCII.

We execute our script and get the following results:

Observing the packet #49, there is a reference to a file named '/tmp/dnscap.png'.

On the other hand, in the packet #50 we see the magic number of a PNG file (89 50 4E 47 0D 0A 1A 0A):
```
49
^A:^A<FD><F5>A}%2^@^@^@^T^@^A^@^C/tmp/dnscap.png^@
49
x^\^A<FD><F5>%2A}
50
<BB><CF>^A<FD><F5>%2A<95>^@^@,<ED><80>^A^@^C<89>PNG
^Z
^@^@^@^MI
```

Contents of packet 50:
```
50      bbcf01fdf52532419500002ced8001000389504e470d0a1a0a0000000d49.48445200000100000001000804000000f67b60ed0000000467414d410001.86a031e8965f00000002624b474400ff878fccbf00000009704859730000.0b1300000b1301009a9c1800000007.skullseclabs.org
```

We know that a PNG file is made of chunks and that in one image of this type we must find at least chunks of the following types: one IHDR (49 48 44 52), one or more IDAT (49 44 41 54) and one IEND (49 45 4E 44).

We look for the IEND chunk and find it on packet #339:
```
339     b8a101fdf551d24195315432313a30343a30302d30383a3030e382804f00.00002574455874646174653a6d6f6469667900323031372d30322d303154.32313a30343a30302d30383a303092df38f30000000049454e44ae426082.skullseclabs.org
```

So we can conclude that most probably there is a PNG image hidden between packets 50 and 339.

-----
## (3) REBUILDING A BINARY FILE

We will try to rebuild a binary file from the extrated hex strings from the payloads of the packets. We modify our script (now 'bsidessf17_dnscap_script2.pl') to dump the extrated hex strings to a file:

```
#!/usr/bin/perl
#
# bsidessf17 - dnscap
#
# script de volcado de datos de paquetes
#
# fusion_ordenado.txt tiene el formato: <paquete>\t<datos>
#
# Rev.20170212 by sn4fu

use strict;
use warnings;
use 5.016;

my $fichero = 'fusion_ordenado.txt';
open(my $fh,$fichero)
or die "No se ha encontrado el fichero '$fichero' $!";

while (my $linea = <$fh>) {
 chomp $linea;										# quitar CR
 my ($paquete, $datos) = split /\t/, $linea;		# parsear usando TAB como separador
 my @cadenas = split /\./, $datos;					# parsear las partes de la cadena de datos separadas con '.'
 my $cadena_sobrante1 = 'org';						# las cadenas 'org' no nos interesan
 @cadenas = grep {!/$cadena_sobrante1/} @cadenas;
 my $cadena_sobrante2 = 'skullseclabs';
 @cadenas = grep {!/$cadena_sobrante2/} @cadenas;	# las cadenas 'skullseclabs' no no sinteresan
 foreach (@cadenas)
   {
      print "$_\n";									# imprimir los contenidos HEX de interés
   }
}
```

We execute the script and dump the results to the 'hex.txt' file:
```
# ./script_dnscap2.pl > hex.txt
```

Due to the fact that this file contains a string on each line, we process the file to delete all carriage returns:
```
# tr -d '\r\n' < hex.txt > hex2.txt
```

And finally we use the 'xxd' utility to convert the hex file to binary:
```
# xxd -p -r hex2.txt > hex2.bin
```






