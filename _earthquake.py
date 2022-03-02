from urllib.request import urlopen
from bs4 import BeautifulSoup
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from pydub import AudioSegment
from pydub.playback import play
from random import randrange
# pip install simpleaudio
# https://mixkit.co/free-sound-effects/

import math
import time


def getValueFromWebSite():
    response = urlopen('http://terremoti.ingv.it/')
    #response = urlopen('https://www.3bmeteo.com/terremoti/italia')
    soup = BeautifulSoup(response.read(), 'html.parser')

    # print(soup.body)
    # print(soup.td)
    # print(soup.find_all('td'))

    for line in soup.find('td', {'class': 'text-center'}).stripped_strings:
        if 'Mwp' in line:
            value = float(line.partition('Mwp')[2])
            if (value != None):
                return(value)
        if 'ML' in line:
            value = float(line.partition('ML')[2])
            if (value != None):
                return(value)


def getValueOnlyFromItalyFromWebSite():
    response = urlopen('http://terremoti.ingv.it/')
    #response = urlopen('https://www.3bmeteo.com/terremoti/italia')
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


def setAudio(intensity):
    # -52 = 2% volume
    # 0 = 100% volume
    if intensity < -52:
        volume = -52
    if intensity > 0:
        volume = 0
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # Get current volume
    currentVolumeDb = volume.GetMasterVolumeLevel()

    volume.SetMasterVolumeLevel(intensity, None)


def playAudio(intensity, path):
    setAudio(intensity)
    song = AudioSegment.from_wav(path)
    play(song)
    # playsound(path)


def test():

    magnitude = randrange(10)
    print(magnitude)
    correction = 0
    MAX_VOLUME = 0
    MIN_VOLUME = -52

    if magnitude < 3:
        playAudio(MIN_VOLUME + correction, 'short.wav')
        playAudio(MIN_VOLUME*6/7 + correction, 'short.wav')
    elif magnitude < 5:
        playAudio(MIN_VOLUME*4/5 + correction, 'short.wav')
    elif magnitude < 6:
        playAudio(MIN_VOLUME/2 + correction, 'short.wav')
    elif magnitude < 7:
        playAudio(MIN_VOLUME/4 + correction, 'short.wav')
    elif magnitude < 8:
        playAudio(MIN_VOLUME/5 + correction, 'short.wav')
    else:
        playAudio(MAX_VOLUME + correction, 'short.wav')

    time.sleep(10)


def application():

    print('world: ' + str(getValueFromWebSite()))
    print('italy: ' + str(getValueOnlyFromItalyFromWebSite()))

    magnitude = float(getValueOnlyFromItalyFromWebSite())
    correction = 0
    MAX_VOLUME = 0
    MIN_VOLUME = -52

    if magnitude < 3:
        playAudio(MIN_VOLUME + correction, 'short.wav')
    elif magnitude < 4:
        playAudio(MIN_VOLUME*6/7 + correction, 'short.wav')
    elif magnitude < 5:
        playAudio(MIN_VOLUME*3/4 + correction, 'short.wav')
    elif magnitude < 6:
        playAudio(MIN_VOLUME/2 + correction, 'short.wav')
    elif magnitude < 7:
        playAudio(MIN_VOLUME/4 + correction, 'short.wav')
    elif magnitude < 8:
        playAudio(MIN_VOLUME/5 + correction, 'short.wav')
    else:
        playAudio(MAX_VOLUME + correction, 'short.wav')

    time.sleep(10)


for i in range(100):
    test()


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
