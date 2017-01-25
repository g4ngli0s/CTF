### ==================================================
### Alienaudio write-up
### CTF: 3DSCTF 2016
### URL: https://3dsctf.win/
### CAT: stego
### ==================================================

In this stego challenge, a tar compressed file is provided. Once decompressed, we get an mp3 file sampled at 44.1 kHz with a rate of 192 kbps and 2 channels (joint stereo):

    $ file 2a30a33063dace93a89d2b3e933fc309.mp3 
    2a30a33063dace93a89d2b3e933fc309.mp3: Audio file with ID3 version 2.3.0, contains: MPEG ADTS, layer III, v1, 192 kbps, 44.1 kHz, JntStereo

If we check the ID3 tag of the mp3 file using any mp3 player, we don't get any useful data.

Listening to all the file with a common mp3 player does not provide any relevant information, just techno music.

Next step is analyzing the file in the frequency domain. In order to do that, we may use several tools such as 'baudline' (Linux):

http://www.baudline.com/

Baudline is able to process files formatted as raw, GSM 6.10 or MPEG. We prefer to work with raw data, so we use the Perl Audio Converter (pacpl) to convert the mp3 file to raw format:

http://vorzox.wixsite.com/pacpl

    $ pacpl --to raw 2a30a33063dace93a89d2b3e933fc309.mp3

According to the baudline documentation:

"Since baudline loads the entire file into RAM, attempting to load a file that is larger than your total memory would result in a lot of swapping.  So in order to prevent this, baudline clamps the maximum file size to be equal to the amount of physical RAM"

Due to the fact that the new raw file is very large, depending on the amount of available RAM we will need to split the file into several pieces (i.e. 4 pieces):

    $ split -n 4 2a30a33063dace93a89d2b3e933fc309.raw

Then we can load each piece separately in baudline, choosing a sample rate of 44100 Hz and 2 channels.  The waterfall of the signal is displayed and we can see the spectrum of the song up to around 11 kHz and a very intense frequency component around 15 kHz. Adjusting the zoom control to the minimum we can see that there is a hidden message in the waterfall spectrum around this frequency:

![](https://github.com/g4ngli0s/pictures/blob/master/3DSCTF_alienaudio_Waterfall_CH1.png)

The resulting flag is:
```
3DS{1_HOp3_Th4t_y0u_h4v3_mut3d_th3_aud10}
```


Note: other useful tool to perform this analysis in Windows environments is 'Sonic Visualiser':

http://sonicvisualiser.org/

Load the file and select: Layer--- Add spectrogram --- all channels mixed

Resulting flag:

    3DS{1_HOp3_Th4t_y0u_h4v3_mut3d_th3_aud10}
