from flask import Flask
from flask import json
app = Flask(__name__)

@app.route("/mood/recommend/<artist>/<song>")
def recommend(artist,song):
  return json.dumps({ 'artist': 'Jay Chou', 'song' : 'Love before BC' })

if __name__ == "__main__":
  app.debug = True
  app.run()
