from data_tr import DataTreatment
from spotify_methods import Spotify
import os

model_data = DataTreatment()

while True:
    print("\n--------RECOMENDADOR DE MÚSICAS--------")
    print("(1) Start!")
    print("(2) Plotar main cluster")
    print("(3) Plotar cluster por genero")
    print("(4) Buscar músicas por artista")
    print("(0) Sair\n")

    opt = int(input())
    os.system('cls')

    if opt == 1:
        print("Artista (igual do spotify):")
        raw_artist = str(input())

        print("Musica (igual do spotify):")
        raw_music = str(input())

        print("\n")

        music = f"{raw_artist} - {raw_music}"

        model = Spotify(music)
        projection = model_data.main_clustering()
        model.recommended_musics(projection)

        os.system('cls')

    elif opt == 2:
        # model_data.ploting_main_cluster()
        continue

    elif opt == 3:
        # model_data.ploting_cluster_by_genre()
        continue

    elif opt == 4:
        print("Artista (igual do spotify):")
        artist = str(input())
        model_data.search_by_artist(artist)

    elif opt == 0:
        break
    else:
        print("Digite um número válido!\n\n")