## ===================================================
## latlong (150 pts)
## CTF: BSidesSF 2017 CTF
## URL: https://scoreboard.ctf.bsidessf.com/
## CAT: forensics
## ===================================================

Transmission Received.

This challenge was created by our pal @arirubinstein . He was not informed of the flag format, so expect this one to be look something like flag{...}
Hint - "Ax25 will lead you in the direction"

'transmission'

-----
## (1) SIGNAL ANALYSIS

In this challenge, a file named 'transmission' is provided, which we can rapidly identify as WAV:
```
# file transmission
transmission: RIFF (little-endian) data, WAVE audio, mono 48000 Hz
```

If you are a ham radio operator and play the file, you don't need more: it is clearly the sound of 1200 bps packet radio. In other words, AX.25 protocol using BFSK modulation at the physical layer.

Just to confirm our hypothesis, we open the file with Audacity and analyze the spectrum:

![alt text](https://github.com/g4ngli0s/pictures/blob/master/bsidessf17_transmission_spectrum.JPG)

In the plot we can see that there are two peaks at 1100 Hz and 2200 Hz, which are the two tones used in BFSK for AX.25.


-----
## (2) SIGNAL DEMODULATION

In order to demodulate this signal, we can use 'multimon-ng':

http://tools.kali.org/wireless-attacks/multimon-ng

After downloading the zip file, follow those steps to install the program and its dependencies:
```
# sudo apt-get install libpulse-dev
# unzip multimon-master-ng.zip
# cd multimon-ng-master
# mkdir build
# cd build
# qmake ../multimon-ng.pro
# make
# sudo make install
```

Before loading the file with 'multimon-ng', we need to perform a conversion from wav format to raw format:
```
# sox -t wav transmission -esigned-integer -b16 -r 22050 -t raw transmission.raw
```

And then proceed with the demodulation:
```
# ./multimon-ng -t raw -a AFSK1200 transmission.raw 
multimon-ng  (C) 1996/1997 by Tom Sailer HB9JNX/AE4WA
             (C) 2012-2014 by Elias Oenal
available demodulators: POCSAG512 POCSAG1200 POCSAG2400 FLEX EAS UFSK1200 CLIPFSK FMSFSK AFSK1200 AFSK2400 AFSK2400_2 AFSK2400_3 HAPN4800 FSK9600 DTMF ZVEI1 ZVEI2 ZVEI3 DZVEI PZVEI EEA EIA CCIR MORSE_CW DUMPCSV SCOPE
Enabled demodulators: AFSK1200
AFSK1200: fm WDPX01-0 to APRS-0 UI  pid=F0
!/;E'q/Sz'O   /A=000000flag{f4ils4f3c0mms}
```

The flag is:
flag{f4ils4f3c0mms}
