from flask import Flask
from flask import json, render_template
import requests
from pygn2 import search, getNodeContent
app = Flask(__name__)

@app.route("/mood/recommend/<artists>/<songs>")
def recommend(artists, songs):
  artists_list = artists.split('&')
  songs_list = songs.split('&')
  artist_data = get_mood_by_artist_and_song(artists_list, songs_list)
  rhythm_input = get_rhythm_api_input(artist_data)
  rhythm_input = get_gerne_mapping(rhythm_input)
  recommend_json = get_recommed_by_metadata(rhythm_input)
  album = recommend_json['RESPONSE'][0]['ALBUM']
  result = get_tempo_filter_result(album, rhythm_input)
  return json.dumps(result)

def get_tempo_filter_result(album, rhythm_input):
  result = {}
  full_match_result = filter(lambda x: x['TRACK'][0]['TEMPO'][0]['VALUE'] == rhythm_input['tempo_speed'], album)
  if len(full_match_result) > 0:
    result['artist'] = full_match_result[0]['ARTIST'][0]['VALUE']
    result['song'] = full_match_result[0]['TRACK'][0]['TITLE'][0]['VALUE']
    result['cover_url'] = full_match_result[0]['URL'][0]['VALUE']
  else:
    tempo_speed = int(rhythm_input['tempo_speed'][:-1])
    map_result = map(lambda x: abs(int(x['TRACK'][0]['TEMPO'][0]['VALUE'][:-1]) - tempo_speed), album)
    min_index = map_result.index(min(map_result))
    result['artist'] = album[min_index]['ARTIST'][0]['VALUE']
    result['song'] = album[min_index]['TRACK'][0]['TITLE'][0]['VALUE']
    result['cover_url'] = album[min_index]['URL'][0]['VALUE']
  return result

def get_gerne_mapping(rhythm_input):
  json_data = json.loads(requests.get(get_genre_api_url()).text)
  genre_list = json_data['RESPONSE'][0]['GENRE']
  genre_list = filter(lambda x: x['VALUE'] == rhythm_input['genre'], genre_list)
  if len(genre_list) > 0:
    rhythm_input['genre'] = genre_list[0]['ID']
  else:
    rhythm_input['genre'] = '36056'
  return rhythm_input

def get_rhythm_api_input(artist_data):
  key_list = list(artist_data[0].keys())
  intersection = dict(set.intersection(*(set(d.iteritems()) for d in artist_data)))
  if len(intersection) < len(key_list):
    for key in key_list:
      if (key in intersection) == False:
        intersection[key] = artist_data[0][key]
  return intersection

def get_recommed_by_metadata(rhythm_input):
  return json.loads(requests.get(get_rhythm_api_url(rhythm_input)).text)

def get_mood_by_artist_and_song(artists_list, songs_list):
  artist_data = []
  for i in range(0, len(artists_list)):
    json_data = get_webapi_url(artists_list[i], songs_list[i])
    metadata = {}
    metadata["mood"] = json_data['RESPONSE']['ALBUM']['TRACK']['MOOD']['1']['ID']
    if ('1' in json_data['RESPONSE']['ALBUM']['ARTIST_ERA']):
       metadata["era"] = json_data['RESPONSE']['ALBUM']['ARTIST_ERA']['1']['ID']
    else:
      metadata["era"] = json_data['RESPONSE']['ALBUM']['ARTIST_ERA']['ID']
    metadata["genre"] = json_data['RESPONSE']['ALBUM']['GENRE']['1']['GENRE']
    metadata["tempo"] = json_data['RESPONSE']['ALBUM']['TRACK']['TEMPO']['1']['ID']
    metadata["tempo_speed"] = json_data['RESPONSE']['ALBUM']['TRACK']['TEMPO']['3']['TEMPO']
    artist_data.append(metadata)
  return artist_data

def get_webapi_url(artist, song):
  input_JSON = {'artist':artist, 'track_title':song, 'select_extended':'MOOD,TEMPO,ARTIST_OET', 'select_detail':'GENRE:3LEVEL,MOOD:2LEVEL,TEMPO:3LEVEL,ARTIST_ORIGIN:4LEVEL,ARTIST_ERA:2LEVEL,ARTIST_TYPE:2LEVEL', 'mode':'SINGLE_BEST'}
  resultDOM = search(clientID='1793280-7808DAD28CB8E790045FC5C0D9F9E962', userID='261582402794837245-41824A367E0E6B5A4BA7816ECF761612', artist=input_JSON['artist'], track=input_JSON['track_title'], input_JSON=input_JSON)
  jsonResponse = {}
  response = resultDOM.getElementsByTagName("RESPONSE")[0]
  jsonResponse = getNodeContent(response)
  return jsonResponse
  #return "http://odp-webdev-401.internal.gracenote.com:5000/album_search?client=1793280-7808DAD28CB8E790045FC5C0D9F9E962&user=261582402794837245-41824A367E0E6B5A4BA7816ECF761612&artist="+artist+"&track_title="+song+"&select_extended=MOOD,TEMPO,ARTIST_OET&select_detail=GENRE:3LEVEL,MOOD:2LEVEL,TEMPO:3LEVEL,ARTIST_ORIGIN:4LEVEL,ARTIST_ERA:2LEVEL,ARTIST_TYPE:2LEVEL&mode=SINGLE_BEST"


def get_rhythm_api_url(rhythm_input):
  return "https://c1793280.web.cddbp.net/webapi/json/1.0/radio/recommend?client=1793280-7808DAD28CB8E790045FC5C0D9F9E962&user=261582402794837245-41824A367E0E6B5A4BA7816ECF761612&genre="+rhythm_input['genre']+"&era="+rhythm_input['era']+"&mood="+rhythm_input['mood']+"&select_extended=tempo,mood,cover&filter_mood="+rhythm_input['mood']

def get_genre_api_url():
  return "https://c1793280.web.cddbp.net/webapi/json/1.0/radio/fieldvalues?client=1793280-7808DAD28CB8E790045FC5C0D9F9E962&user=261582402794837245-41824A367E0E6B5A4BA7816ECF761612&fieldname=radiogenre"

@app.route("/recmd")
def recmd():
  return render_template('test.html')

if __name__ == "__main__":
  app.debug = True
  app.run()
