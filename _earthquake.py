from urllib.request  import urlopen
from bs4 import BeautifulSoup
import time

def getValueFromWebSite():
    response = urlopen('http://terremoti.ingv.it/')
    #response = urlopen('https://www.3bmeteo.com/terremoti/italia')
    soup = BeautifulSoup(response.read(),'html.parser')

    #print(soup.body)
    #print(soup.td)
    #print(soup.find_all('td'))


    for line in soup.find('td', {'class': 'text-center'}).stripped_strings:
        if 'Mwp' in line:
            value = float(line.partition('Mwp')[2])
            if (value!=None):
                return(value)
        if 'ML' in line:
            value = float(line.partition('ML')[2])
            if (value!=None):
                return(value)


def getValueOnlyFromItalyFromWebSite():
    response = urlopen('http://terremoti.ingv.it/')
    #response = urlopen('https://www.3bmeteo.com/terremoti/italia')
    soup = BeautifulSoup(response.read(),'html.parser')

    #print(soup.body)
    #print(soup.td)
    #print(soup.find_all('td'))

    lines = soup.find_all('td', {'class': 'text-center'})

    for line in lines:
        if 'ML' in line.get_text():
            value = float(line.get_text().partition('ML')[2])
            if (value!=None):
                return(value)


for i in range(100):
    print('world: ' + str(getValueFromWebSite()))
    print('italy: ' + str(getValueOnlyFromItalyFromWebSite()))
    time.sleep(20)




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