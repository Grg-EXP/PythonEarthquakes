from urllib.request import urlopen
from bs4 import BeautifulSoup
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pydub import AudioSegment
from pydub.playback import play
from random import randrange
import sys
import getopt
# pip install simpleaudio
# https://mixkit.co/free-sound-effects/

import math
import time
import threading

def getValueFromWebSite():
    try:
        response = urlopen('http://terremoti.ingv.it/')
        # response = urlopen('https://www.3bmeteo.com/terremoti/italia')
        soup = BeautifulSoup(response.read(), 'html.parser')
        for line in soup.find('td', {'class': 'text-center'}).stripped_strings:
            if 'Mwp' in line:
                value = float(line.partition('Mwp')[2])
                if (value != None):
                    return value
            if 'ML' in line:
                value = float(line.partition('ML')[2])
                if (value != None):
                    return value           
    except:
        print("Errore di connessione al sito, assicurati di essere connesso ad internet")
        return 0.0
    # print(soup.body)
    # print(soup.td)
    # print(soup.find_all('td'))

    

def getIDFromWebSite():
    try:
        response = urlopen('http://terremoti.ingv.it/')
        soup = BeautifulSoup(response.read(), 'html.parser')
        return str(soup.td)
    except:
        print("Errore di connessione al sito, assicurati di essere connesso ad internet")
        return ""


'''
def getValueOnlyFromItalyFromWebSite():
    response = urlopen('http://terremoti.ingv.it/')
    # response = urlopen('https://www.3bmeteo.com/terremoti/italia')
    soup = BeautifulSoup(response.read(), 'html.parser')

    # print(soup.body)
    # print(soup.td)
    # print(soup.find_all('td'))

    lines = soup.find_all('td', {'class': 'text-center'})

    for line in lines:
        if 'ML' in line.get_text():
            value = float(line.get_text().partition('ML')[2])
            if (value != None):
                return(value)
'''

def speed_change(sound, speed=1.0):  
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def setAudio(intensity):
    # -52 = 2% volume
    # -0 = 100% volume
    if intensity < -52:
        intensity = -52
    elif intensity > 0:
        intensity = -0
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        currentVolumeDb = volume.GetMasterVolumeLevel()
        volume.SetMasterVolumeLevel(intensity, None)
    except:
        print("Errore nella rilevazione del dispositivo audio, intensity: " + str(intensity))
        

def playSong(path):
    try:
        song = AudioSegment.from_wav(path)
        play(song)
    except:
        print("errore nella riproduzione della traccia audio, verificare di avere inserito il file audio con il nome corretto")


def playAudio(intensity, path):
    setAudio(intensity)
    playSong(path)
    

def test(audiopath, correction):

    for i in range(1,10):
            application(audiopath, correction,i)
            time.sleep(1)

def application(audiopath, correction, magnitude):

    MIN_VOLUME = -52
    VOLUME4 = -32
    VOLUME5 = -22
    VOLUME6 = -18
    VOLUME7 = -14
    VOLUME8 = -7
    MAX_VOLUME = -0
    correction = int(correction)

    print("magnitudo rilevata: " +str(magnitude))
    if magnitude < 3:
        playAudio(MIN_VOLUME + correction, audiopath)
    elif magnitude < 4:
        playAudio(VOLUME4 + correction, audiopath)
    elif magnitude < 5:
            playAudio(VOLUME5 + correction, audiopath)
    elif magnitude < 6:
        playAudio(VOLUME6 + correction, audiopath)
    elif magnitude < 7:
            playAudio(VOLUME7 + correction, audiopath)
    elif magnitude < 8:
        playAudio(VOLUME8 + correction, audiopath)
    else:
        playAudio(MAX_VOLUME , audiopath)


if __name__ == "__main__":
    #test
    if len(sys.argv) > 3:       
        test(sys.argv[1], sys.argv[2])
        
    body2=""
    while True:
        body1=getIDFromWebSite()
        print("Ultimo terremoto registrato: + " + body1)

        if(body1!=body2):      
            application(sys.argv[1], sys.argv[2], float(getValueFromWebSite()))
            body2=getIDFromWebSite()
        
        time.sleep(10)        

'''

3.0–3.9	minor	felt by many people; no damage	12,000–100,000
4.0–4.9	light	felt by all; minor breakage of objects	2,000–12,000
5.0–5.9	moderate	some damage to weak structures	200–2,000
6.0–6.9	strong	moderate damage in populated areas	20–200
7.0–7.9	major	serious damage over large areas; loss of life	3–20
8.0 and higher	great	severe destruction and loss of life over large areas	fewer than 3
'''

'''
<div class="panel-body">
<tr class="" data-href="http://terremoti.ingv.it/event/29389071">
						<td class="text-nowrap "><a href="http://terremoti.ingv.it/event/29389071">2022-01-03&nbsp;09:36:34 </a>

												</td>
						<td class="text-center "><a href="http://terremoti.ingv.it/event/29389071"> ML&nbsp;2.4</a></td>
						<td class=""><a href="http://terremoti.ingv.it/event/29389071">8 km NW Arquata del Tronto (AP)</a></td>
						<td class="hidden-xs text-right"><a href="http://terremoti.ingv.it/event/29389071">9</a></td>
						<td class="hidden-xs hidden-sm text-right"><a href="http://terremoti.ingv.it/event/29389071">42.83</a></td>
						<td class="hidden-xs hidden-sm text-right"><a href="http://terremoti.ingv.it/event/29389071">13.23</a></td>

						</tr>
'''
