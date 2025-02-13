
from flask import Flask, redirect, request, url_for, render_template,session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#le tue credenziali le trovi nella dashboard di prima
SPOTIFY_CLIENT_ID = "443883fd510c43e29bb9ee1e295cddd5"
SPOTIFY_CLIENT_SECRET = "f6de4aa660244f8d8689aea1b94344de"
SPOTIFY_REDIRECT_URI = "https://5000-kimpembie2-spotibie-ofw7qd187r1.ws-eu117.gitpod.io/callback"

app = Flask(__name__)
app.secret_key = 'chiave_per_session'

sp_oauth = SpotifyOAuth(
client_id=SPOTIFY_CLIENT_ID,
client_secret=SPOTIFY_CLIENT_SECRET,
redirect_uri=SPOTIFY_REDIRECT_URI,
scope="user-read-private",
show_dialog=True #forziamo la richiesta di inserire new credenziali
)


@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url() 
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info 
    return redirect(url_for('home'))

@app.route('/home')
def home():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    print(user_info) 
    playlists = sp.current_user_playlists() #sempre tramite il token sp preso prima
    playlists_info = playlists['items'] #prendiamo solo la lista delle playlist
    return render_template('home.html', user_info=user_info, playlists=playlists_info) 

@app.route('/playlist/<playlist_id>')
def playlist_details(playlist_id):
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    brani = sp.playlist_items(playlist_id)
    brani_specifici = brani['items']
    return render_template('brani.html',brani = brani_specifici)



@app.route('/logout')
def logout():
    session.clear() #cancelliamo l'access token salvato in session
    return redirect(url_for('login'))

if __name__ == '__main__': 
    
    app.run(debug=True)
