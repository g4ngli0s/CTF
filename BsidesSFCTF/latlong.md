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

In this challenge, a file named 'transmission' is provided, which we can rapidly identify as WAV:
```
# file transmission
transmission: RIFF (little-endian) data, WAVE audio, mono 48000 Hz
```

If you are a ham radio operator and play the file, you don't need more: it is clearly the sound of 1200 bps packet radio. In other words, AX.25 protocol using BFSK modulation at the physical layer.

Just to confirm our hypothesis, we open the file with Audacity and analyze the spectrum:

![alt text](https://github.com/g4ngli0s/pictures/blob/master/bsidessf17_transmission_spectrum.JPG)

In the plot we can see that there are two peaks at 1100 Hz and 2200 Hz, which are the two tones used in BFSK for AX.25.
