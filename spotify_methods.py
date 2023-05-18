import spotipy
import os
from dotenv import load_dotenv

class Spotify:
  def __init__(self, music_name):
    load_dotenv()
    self.music_name = music_name

    scope = 'user-library-read playlist-modify-private'
    client_id = os.environ['SP_CLIENT_ID']
    client_secret = os.environ['SP_CLIENT_SECRET']

    OAuth = spotipy.oauth2.SpotifyOAuth(
        scope=scope,
        redirect_uri= 'http://localhost:8888/callback',
        client_id= client_id,
        client_secret=client_secret,
    )

    client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

  def visualize_songs(self, names, images_url):
    import matplotlib.pyplot as plt
    from skimage import io

    # plt.figure(figsize=(15,10))
    columns = 5
    for i, u in enumerate(images_url):
        ax = plt.subplot(len(images_url) // columns + 1, columns, i + 1)
        image = io.imread(u)
        plt.imshow(image)
        ax.get_yaxis().set_visible(False)
        plt.xticks(color = 'w', fontsize = 0.1)
        plt.yticks(color = 'w', fontsize = 0.1) 
        plt.xlabel(names[i], fontsize = 8)
        plt.tight_layout(h_pad=0.7, w_pad=0)
        plt.subplots_adjust(wspace=None, hspace=None)
        plt.tick_params(bottom = False)
        plt.grid(visible=None)

    print("Quando terminar a análise feche o app!")
    plt.show()

  def spotify_push(self, playlist_ids):
    images_url = []
    names = []
    artists = []
    duration = []
    for i in playlist_ids:
        track = self.sp.track(i)
        images_url.append(track["album"]["images"][1]["url"])
        names.append(track["name"])
        artists.append(track["artists"][0]["name"])
        duration.append(round(track["duration_ms"]/60000, 2))

    return names, images_url, artists, duration
     

  def recommended_musics(self, projection_m):
    from sklearn.metrics.pairwise import euclidean_distances

    try:
      cluster = list(projection_m[projection_m['song']== self.music_name]['cluster_pca'])[0]
    except:
      print("Musica nao encontrada na database!\n\n")
      return 0
    
    recommended_musics_raw = projection_m[projection_m['cluster_pca']==cluster][[0, 1, 'song']]
    x_music = list(projection_m[projection_m['song']== self.music_name][0])[0]
    y_music = list(projection_m[projection_m['song']== self.music_name][1])[0]

    distancias = euclidean_distances(recommended_musics_raw[[0, 1]], [[x_music, y_music]])
    recommended_musics_raw['id'] = projection_m['id']
    recommended_musics_raw['distancias'] = distancias

    recommended_musics = recommended_musics_raw.sort_values('distancias').head(10)

    playlist_ids = recommended_musics['id']

    names, images_url, artists, duration = self.spotify_push(playlist_ids)
    
    self.visualize_songs(names, images_url)

  

