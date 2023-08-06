import json
import requests

class shazamLyric:

  result = ''

  def __init__(self,text,rows,offset,country):
    self.text = text
    self.rows = rows
    self.offset = offset
    self.country = country
    self.search()

  def search(this_object):
    url  = f"https://www.shazam.com/services/search/v3/pt/BR/web/search?"
    url += f"query={this_object.text}&"
    url += f"numResults={this_object.rows}&"
    url += f"offset={this_object.offset}&"
    url += f"types=songs"
    payload={}
    headers = {'Cookie':f'geoip_country={this_object.country}'}
    response = requests.request("GET", url, headers=headers, data=payload)
    this_object.result = json.loads(response.text)
    return this_object.result

  def key(this_object):
    lst = []
    txt = this_object.result['tracks']['hits']
    num = len(txt)
    for x in range(num):
      lst.append(txt[x]['key'])
    return lst

  def title(this_object):
    lst = []
    txt = this_object.result['tracks']['hits']
    num = len(txt)
    for x in range(num):
      lst.append(txt[x]['heading']['title'])
    return lst

  def subtitle(this_object):
    lst = []
    txt = this_object.result['tracks']['hits']
    num = len(txt)
    for x in range(num):
      lst.append(txt[x]['heading']['subtitle'])
    return lst

  def lyrics(this_object):
    lst = []
    for x in this_object.key():
      url  = f"https://www.shazam.com/discovery/v5/pt/BR/web/-/track/"
      url += f"{x}?shazamapiversion=v3&video=v3"
      response = requests.request("GET", url, headers={}, data={})
      try:
        lst.append(json.loads(response.text)['sections'][1]['text'])
      except:
        lst.append(['No lyric'])
    return lst

  def youtubeurl(this_object):
    lst = []
    for x in this_object.key():
      url  = f"https://www.shazam.com/discovery/v5/pt/BR/web/-/track/"
      url += f"{x}?shazamapiversion=v3&video=v3"
      response = requests.request("GET", url, headers={}, data={})
      try:
        lst.append(json.loads(response.text)['sections'][2]['youtubeurl'])
      except:
        lst.append('No youtube')
    return lst

  def youtube(this_object):
    lst = []
    for x in this_object.youtubeurl():
      if x != 'No youtube':
        response = requests.request("GET", x, headers={}, data={})
        lst.append(json.loads(response.text)['actions'][0]['uri'])
      else:
        lst.append('No youtube')
    return lst
