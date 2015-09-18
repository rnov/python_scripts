__author__ = 'p45'
__author__ = 'bobby'
# Note: every page it retrieves contains 20 links to bananas(torrents) but not every
#       banana has a link to youtube.
from multiprocessing import Process
import re
import urllib
import timeit
from bs4 import BeautifulSoup, SoupStrainer


zamunda = 'http://zamunda.net/bananas'
zamunda_net = 'http://zamunda.net/{}'
zamunda_pages = 'http://zamunda.net/bananas?field=name&page={}'
youtube = 'https://www.youtube.com/watch?v={}'

list_videos = []


# gets the url from each banana (multiprocess)
def get_video_link(banana_link):
    global list_videos
    htmlResponse = urllib.urlopen(banana_link)
    html = htmlResponse.read().decode('utf-8', 'ignore')
    bs = BeautifulSoup(html, 'lxml')
    code = bs.find('a', {'code': re.compile('.+')})

    if code:
        link = youtube.format(code['code'])
        list_videos.append(link)
        #print p.pid
        print link


# gets the torrents from zamunda/bananas
def get_list_bananas():
    table_tag = SoupStrainer('table', attrs={'class': 'test responsivetable'})
    bs2 = BeautifulSoup(html, 'lxml', parse_only=table_tag)
    return bs2.find_all('a', {'target': '_top', 'onmouseout': 'UnTip();'})


start = timeit.default_timer()

# get the max number of pages
htmlResponse = urllib.urlopen(zamunda)
html = htmlResponse.read().decode('utf-8', 'ignore')
form_tag = SoupStrainer('form', {'style': 'display: inline;'})
bs = BeautifulSoup(html, 'lxml', parse_only=form_tag)
b = bs.find('input', id='gotopage')
print b['max']  # prints number of pages, 20 'bananas' per page

list_pages = [zamunda_pages.format(i) for i in range(0, 20)]  # range(0, b['max']+1)

while list_pages:
    htmlResponse = urllib.urlopen(list_pages.pop(0))
    html = htmlResponse.read().decode('utf-8', 'ignore')

    # getting each link to torrent
    for i in get_list_bananas():
        banana_link = zamunda_net.format(i['href'])

        p = Process(target=get_video_link, args=(banana_link,))  # multiprocess
        p.start()

        #get_video_link(banana_link)  # run one process

stop = timeit.default_timer()
print '{0:.3f} sec.'.format(stop - start)
