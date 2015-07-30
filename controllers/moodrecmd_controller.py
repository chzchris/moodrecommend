from flask import Flask
from flask import json
import requests
app = Flask(__name__)

@app.route("/mood/recommend/<artists>/<songs>")
def recommend(artists, songs):
  artists_list = artists.split('&')
  songs_list = songs.split('&')
  moods = get_mood_by_artist_and_song(artists_list, songs_list)
  recommend_json = get_recommed_by_moods(moods)
  print len(recommend_json['RESPONSE'])
  result = {}
  result['artist'] = recommend_json['RESPONSE'][0]['ALBUM'][0]['ARTIST'][0]['VALUE']
  result['song'] = recommend_json['RESPONSE'][0]['ALBUM'][0]['TITLE'][0]['VALUE']
  return json.dumps(result)

def get_recommed_by_moods(moods):
  return json.loads(requests.get(get_rhythm_api_url(moods)).text)


def get_mood_by_artist_and_song(artists_list, songs_list):
  moods = []
  for i in range(0, len(artists_list)):
    json_data = json.loads(requests.get(get_webapi_url(artists_list[i], songs_list[i])).text)
    moods.append(json_data['RESPONSE']['ALBUM']['TRACK']['MOOD']['ID'])
  return moods

def get_webapi_url(artist, song):
  return "http://odp-webdev-401.internal.gracenote.com:5000/album_search?client=1793280-7808DAD28CB8E790045FC5C0D9F9E962&user=261582402794837245-41824A367E0E6B5A4BA7816ECF761612&artist="+artist+"&track_title="+song+"&select_extended=MOOD&mode=SINGLE_BEST"

def get_rhythm_api_url(moods):
  mood_str = ""
  for i in range(0, len(moods)):
    if i == 0:
      mood_str += "(mood_"+moods[i]+")"
    else:
      mood_str += ";(mood_"+moods[i]+")"
  print mood_str
  return "https://c1793280.web.cddbp.net/webapi/json/1.0/radio/recommend?client=1793280-7808DAD28CB8E790045FC5C0D9F9E962&user=261582402794837245-41824A367E0E6B5A4BA7816ECF761612&seed="+mood_str+"&select_extended=cover"

if __name__ == "__main__":
  app.debug = True
  app.run()
