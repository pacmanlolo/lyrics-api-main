from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import os
import musixmatch

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing if needed

# Retrieve the Musixmatch API key from environment variables
apikey = os.environ.get('MUSIXMATCH_API_KEY')

# Route for the home page
@app.route('/')
def home():
    return redirect("https://api.musixmatch.com/ws/1.1/")

# Route for getting lyrics based on title and artists
@app.route('/getlyrics/')
def get_lyrics():
    title = request.args.get('title')
    artist = request.args.get('artist')
    
    # Check if title and artist parameters are provided
    if not title or not artist:
        return jsonify({"error": "Please provide both 'title' and 'artist' parameters."})

    try:
        # Initialize Musixmatch with your API key
        musixmatch_ws = musixmatch.WebService(apikey=apikey)

        # Search for lyrics
        lyrics = musixmatch_ws.track.search(q_track=title, q_artist=artist, f_has_lyrics=1, page_size=1)
        
        if lyrics:
            # Extract the lyrics from the search result
            lyrics_body = lyrics['message']['body']['track_list'][0]['track']['lyrics']['lyrics_body']
            return jsonify({"lyrics": lyrics_body})
        else:
            return jsonify({"error": "Lyrics not found for the provided title and artist."})
    except musixmatch.api.Error as e:
        return jsonify({"error": "Musixmatch API error: " + str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
