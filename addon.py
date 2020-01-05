import sys
import web_pdb
import xbmcgui
import xbmcplugin
import xbmcaddon

import urlparse
import urlresolver
import sys, urllib

import requests

from os import walk

print('I can log this - ') 
print(sys.argv)

kodi_url = sys.argv[0]
print(kodi_url)
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

def buildURL(query):
    return kodi_url + '?' + urllib.urlencode(query)

def fixURL(url):
    url = url.split("?")[1]
    params = {x[0] : x[1] for x in [x.split("=") for x in url[1:].split("&") ]}
    return params['videoid']    

def fixStreamURL(url):
    videoId = fixURL(url)
    return "plugin://plugin.video.youtube/play/?video_id="+videoId

def resolveURL(url):
    streamingURL = urlresolver.HostedMediaFile(url=url).resolve()
    # web_pdb.set_trace()
    streamingURL = fixStreamURL(streamingURL)
    
    # If urlresolver returns false then the video url was not resolved.
    if not streamingURL:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Failed", "Unable to play video", xbmcgui.NOTIFICATION_INFO, 6000)
        return False
    else:        
        return streamingURL  

def playContent(contentPath):

    play_item = xbmcgui.ListItem(path=contentPath)
    vid_url = play_item.getfilename()
    stream_url = resolveURL(vid_url)
    if stream_url:
        play_item.setPath(stream_url)

    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

# When user executes kodi the following line begins execution
mode = args.get('action', None)
# web_pdb.set_trace()

if mode is None:
    url = buildURL({'action' :'trending'})
    li = xbmcgui.ListItem('Trending Videos')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    # url = buildURL({'action' :'webcam'})
    # li = xbmcgui.ListItem('Webcam Videos')
    # xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'trending':
    g_api_url = "https://content.googleapis.com/youtube/v3/videos"

    querystring = {"chart":"mostPopular","part":"contentDetails,snippet","regionCode":"US","key":"AIzaSyAMjgkUr4crwty4Vo72rfQjet0mgNyDHOI"}

    headers = {
        'cache-control': "no-cache",
        'postman-token': "822a80a7-635b-0f83-7569-6bfae3b7010a"
        }

    response = requests.request("GET", g_api_url, headers=headers, params=querystring)
    items = response.json()['items']
    i = 0
    for each in items:
        videoId =  each['id']
        video_play_url = "https://www.youtube.com/watch?v=" + videoId
        url = buildURL({'action' :'play', 'playlink' : video_play_url})
        snippet = each['snippet']
        title = snippet['title']
        thumbnail = snippet['thumbnails']['default']['url']
        li = xbmcgui.ListItem(title, iconImage=thumbnail)
        li.setInfo('video', {'Title': title})
        li.setProperty('IsPlayable' , 'true')
        i+=1
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    
    xbmcplugin.endOfDirectory(addon_handle)

# elif mode[0] == 'webcam':
#     url = 'http://localhost:8070/dolbycanyon.mkv'
#     li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png')
#     li.setInfo('video', {'Title': 'First'})
#     xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
#     xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play':
    # web_pdb.set_trace()
    playLink = args['playlink'][0]
    playContent(playLink)