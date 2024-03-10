# Importing all necessary libraries
import numpy as np
import pandas as pd

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity

# Spotify Developer Credential Info
spotify_client_id = "01385e98a17747c58c71ebdf6c755f58"
spotify_client_secret = "89c5965b40484437ae9a13c53af6ca9a"
client_credentials_manager = SpotifyClientCredentials(
    client_id=spotify_client_id, client_secret=spotify_client_secret)
sp = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager, language="en")

username = ""


def set_username(api_username):
    """
    Sets the global username for Spotify API interactions.
    
    Parameters:
    - api_username: Spotify username of the user
    """
    global username
    username = api_username


def fetch_user_playlists(username):
    """
    Fetches user's playlists using Spotify API.
    
    Parameters:
    - username: Spotify username of the user
    
    Returns:
    Tuple of lists containing playlist names, IDs, and cover image URLs.
    """
    try:
        playlists = sp.user_playlists(username)
    except:
        return False
    playlist_ids, playlist_names, playlist_images = [], [], []
    while playlists:
        for playlist in playlists['items']:
            print(
                f"Playlist Name: {playlist['name']}, Playlist Id: {playlist['id']}")
            playlist_ids.append(playlist['id'])
            playlist_names.append(playlist['name'])
            if len(playlist['images']) > 0:
                playlist_images.append(playlist['images'][0]['url'])
            else:
                playlist_images.append("./logo.svg")
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
        return playlist_names, playlist_ids, playlist_images


def generate_user_track_metadata_df(playlist_ids):
    """
    Generates a dataframe with metadata for each track in user's playlists.
    
    Parameters:
    - playlist_ids: List of Spotify playlist IDs
    
    Returns:
    Tuple of list of song IDs and a dataframe with song metadata.
    """
    songs_names, songs_ids, songs_album, songs_artist, songs_length, songs_popularity, artist_genres, release_dates = [
    ], [], [], [], [], [], [], []
    artist_genres_lookup = dict()  # cache
    for idx, playlist_id in enumerate(playlist_ids):
        playlist = sp.user_playlist('spotify', playlist_id)
        for item in playlist['tracks']['items']:
            track = item['track']
            if track['id'] is None:
                continue  # if song is no longer on spotify
            songs_names.append(track['name'])  # song name
            songs_ids.append(track['id'])  # spotify song id
            songs_album.append(track['album']['name'])  # song album
            try:
                songs_artist.append(
                    track['album']['artists'][0]['name'])  # song artist
            except:
                # for remixes missing artists
                songs_artist.append("Artist Not Found")

            # artist genre
            if track['album']['artists'][0]["id"] in artist_genres_lookup:
                artist_genres.append(
                    artist_genres_lookup[track['album']['artists'][0]["id"]])
            else:
                artist_genres_lookup[track['album']['artists'][0]["id"]] = sp.artist(
                    track['album']['artists'][0]["id"])["genres"]
                artist_genres.append(
                    artist_genres_lookup[track['album']['artists'][0]["id"]])

            songs_length.append(track['duration_ms'])  # song length (ms)
            songs_popularity.append(track['popularity'])  # song popularity
            # song album release date
            release_dates.append(track['album']['release_date'])

    return songs_ids, pd.DataFrame({"song_name": songs_names,
                                    "album": songs_album,
                                    "spotify_id": songs_ids,
                                    "artist": songs_artist,
                                    "release_dates": release_dates,
                                    "genres": artist_genres,
                                    "length": songs_length,
                                    "popularity": songs_popularity})


def generate_user_track_audio_features_df(songs_ids):
    """
    Generates a dataframe with audio features for each track identified by the song IDs.
    
    Parameters:
    - songs_ids: List of Spotify song IDs
    
    Returns:
    A dataframe containing audio features like acousticness, danceability, etc., for each track.
    """
    acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature = [
    ], [], [], [], [], [], [], [], []
    ids_count = len(songs_ids)
    p1, p2 = 0, 100
    for increment in range(0, len(songs_ids), 100):
        if p2 >= ids_count:
            p2 = ids_count
        songs_features = sp.audio_features(
            tracks=songs_ids[p1:p2])  # max limit: 100
        for features in songs_features:
            acousticness.append(features['acousticness'])
            danceability.append(features['danceability'])
            energy.append(features['energy'])
            instrumentalness.append(features['instrumentalness'])
            liveness.append(features['liveness'])
            loudness.append(features['loudness'])
            speechiness.append(features['speechiness'])
            tempo.append(features['tempo'])
            time_signature.append(features['time_signature'])
        p1 += 100
        p2 += 100

    return pd.DataFrame({"acousticness": acousticness,
                         "danceability": danceability,
                         "energy": energy,
                         "instrumentalness": instrumentalness,
                         "liveness": liveness,
                         "loudness": loudness,
                         "speechiness": speechiness,
                         "tempo": tempo,
                         "time_signature": time_signature})


def generate_user_dfs(df_meta, df_features):
    """
    Combines track metadata and audio features into a unified dataframe, performs data cleanup, and splits release dates.
    
    Parameters:
    - df_meta: Dataframe containing track metadata
    - df_features: Dataframe containing track audio features
    
    Returns:
    A tuple containing the combined dataframe and a separate dataframe with split release date components.
    """
    user_all_df = pd.concat([df_meta, df_features], axis=1)
    print("User_All_Df")
    print(user_all_df)

    print(
        f"Number of User Songs before Dropping Duplicates: {len(user_all_df)}")
    user_all_df = user_all_df.drop_duplicates(subset=['song_name'])
    print(
        f"Number of User Songs after Dropping Duplicates: {len(user_all_df)}")

    user_date_df = user_all_df["release_dates"].str.split("-", expand=True)
    user_date_df.columns = ["year", "month", "day"]

    return user_all_df, user_date_df


def generate_recommendations_dfs(user_all_df):
    """
    Generates recommended songs based on the user's most listened genres and release times, and creates dataframes for recommendations.
    
    Parameters:
    - user_all_df: Dataframe containing user's songs data
    
    Returns:
    A tuple of two dataframes: one with recommended songs' metadata and another with split release date components.
    """

    most_listened_genres = user_all_df['genres'].explode(
    ).value_counts().head(8).index.tolist()
    date_df = user_all_df["release_dates"].str.split("-", expand=True)
    date_df.columns = ["year", "month", "day"]
    reco_song_names = []

    for genre in most_listened_genres:
        typical_time_period_by_genre = date_df['year'][user_all_df[user_all_df == genre].index].value_counts(
        ).head(4).index.tolist()
        for time_period in typical_time_period_by_genre:
            possible_reco_songs = sp.search(
                q='genre:' + genre + time_period, type='track', limit=50, market="US")  # max = 50
            for track in possible_reco_songs['tracks']['items']:
                if track["name"] in user_all_df['song_name'].values:
                    continue
                reco_song_names.append(track['name'])  # reco song names

    reco_song_names = list(set(reco_song_names))
    reco_artist_genres_lookup = dict()  # cache

    reco_song_ids, reco_artist_genres, reco_songs_artists, reco_songs_albums, reco_songs_len, reco_songs_pop, reco_songs_release_dates = [], [], [], [], [], [], []
    for track_name in reco_song_names:
        reco_search = sp.search(q=f"{track_name}", type="track", limit=1)
        if reco_search:
            top_track = reco_search['tracks']['items'][0]
            if top_track is None:
                continue
            reco_song_ids.append(top_track['id'])  # reco spotify song id
            # reco song length (ms)
            reco_songs_len.append(top_track['duration_ms'])
            # reco song popularity
            reco_songs_pop.append(top_track['popularity'])
            # reco song album release date
            reco_songs_release_dates.append(top_track['album']['release_date'])
            reco_songs_albums.append(top_track['album']['name'])  # song album
            try:
                reco_songs_artists.append(
                    top_track['album']['artists'][0]['name'])  # reco song artist
            except:
                # for reco remixes missing artists
                reco_songs_artists.append("Artist Not Found")
            # reco artist genre
            if top_track['album']['artists'][0]["id"] in reco_artist_genres_lookup:
                reco_artist_genres.append(
                    reco_artist_genres_lookup[top_track['album']['artists'][0]["id"]])
            else:
                reco_artist_genres_lookup[top_track['album']['artists'][0]["id"]] = sp.artist(
                    top_track['album']['artists'][0]["id"])["genres"]
                reco_artist_genres.append(
                    reco_artist_genres_lookup[top_track['album']['artists'][0]["id"]])

    no_audio_features_indices = []
    reco_acousticness, reco_danceability, reco_energy, reco_instrumentalness, reco_liveness, reco_loudness, reco_speechiness, reco_tempo, reco_time_signature = [], [], [], [], [], [], [], [], []
    ids_count = len(reco_song_ids)
    p1, p2 = 0, 100

    for increment in range(0, len(reco_song_ids), 100):
        if p2 >= ids_count:
            p2 = ids_count
        reco_songs_features = sp.audio_features(
            tracks=reco_song_ids[p1:p2])  # max limit: 100
        for i, features in enumerate(reco_songs_features):
            if not features:
                no_audio_features_indices.append(p1 + i)
                continue
            reco_acousticness.append(features['acousticness'])
            reco_danceability.append(features['danceability'])
            reco_energy.append(features['energy'])
            reco_instrumentalness.append(features['instrumentalness'])
            reco_liveness.append(features['liveness'])
            reco_loudness.append(features['loudness'])
            reco_speechiness.append(features['speechiness'])
            reco_tempo.append(features['tempo'])
            reco_time_signature.append(features['time_signature'])
        p1 += 100
        p2 += 100

    no_audio_features_indices.sort(reverse=True)
    for i in no_audio_features_indices:
        reco_song_names.pop(i)

    print("Check for Uneven Reco_Meta_Df:")
    print(f"Song Names Length: {len(reco_song_names)}")
    print(f"Ids Length: {len(reco_song_ids)}")

    reco_meta_df = pd.DataFrame({"song_name": reco_song_names,
                                 "found_location": reco_songs_albums,
                                 "spotify_id": reco_song_ids,
                                 "found_publisher": reco_songs_artists,
                                 "release_dates": reco_songs_release_dates,
                                 "genres": reco_artist_genres,
                                 "length": reco_songs_len,
                                 "popularity": reco_songs_pop})

    reco_audio_features_df = pd.DataFrame({"acousticness": reco_acousticness,
                                           "danceability": reco_danceability,
                                           "energy": reco_energy,
                                           "instrumentalness": reco_instrumentalness,
                                           "liveness": reco_liveness,
                                           "loudness": reco_loudness,
                                           "speechiness": reco_speechiness,
                                           "tempo": reco_tempo,
                                           "time_signature": reco_time_signature})

    reco_all_df = pd.concat([reco_meta_df, reco_audio_features_df], axis=1)
    print("Reco All Df")
    print(reco_all_df[reco_all_df.isnull().any(axis=1)])

    # Dropping Duplicates in all recommended songs dataset using recommended song ids
    print(
        f"Number of Reco Songs before Dropping Duplicates: {len(reco_all_df)}")
    reco_all_df = reco_all_df.drop_duplicates(subset=['spotify_id'])
    print(
        f"Number of Reco Songs after Dropping Duplicates: {len(reco_all_df)}")

    reco_date_df = reco_all_df["release_dates"].str.split("-", expand=True)
    reco_date_df.columns = ["year", "month", "day"]

    return reco_all_df, reco_date_df


def feature_engineering(user_all_df, reco_all_df, user_date_df, reco_date_df):
    """
    Performs feature engineering on the combined dataset of user and recommended songs.
    
    Parameters:
    - user_all_df: Dataframe of user's songs
    - reco_all_df: Dataframe of recommended songs
    - user_date_df: Dataframe of user's song release dates
    - reco_date_df: Dataframe of recommended song release dates
    
    Returns:
    A tuple of dataframes for user and recommended songs with features engineered for model processing.
    """
    print("Feature Engineering...")
    # Vertical Concatenation of User Playlists and Recommendations Dataframes
    all_df = pd.concat([user_all_df, reco_all_df], axis=0, ignore_index=True)
    all_date_df = pd.concat([user_date_df, reco_date_df],
                            axis=0, ignore_index=True)

    print("All Date Df Null Check")
    print(all_df[all_df.isnull().any(axis=1)])

    # Removing features for system that could cause data leakage
    model_df = all_df.copy(deep=True)
    model_df = model_df.drop(columns=["song_name",	"album",	"spotify_id",	"artist",
                             "release_dates", "genres", "found_location", "found_publisher"])

    # Float Features Normalization using MinMaxScaler
    print("Normalized Data")
    scaler = MinMaxScaler()
    scaler.set_output(transform="pandas")
    model_df = scaler.fit_transform(model_df)
    print(model_df)

    # One Hot Encoding (OHE) of Date Features
    print("OHE Data")
    ohe_df = pd.get_dummies(all_date_df, columns=['year', 'month', 'day'])
    print(ohe_df)

    # Removing Non-Iterable Values in Genres
    all_df['genres'] = all_df['genres'].apply(
        lambda x: x if isinstance(x, list) else [])

    print("TFIDF")
    # Term Frequency - Inverse Document Frequency (TFIDF) for Song Genres
    tfidf = TfidfVectorizer()
    tfidf_genres = tfidf.fit_transform(
        all_df['genres'].apply(lambda genres: " ".join(genres)))
    genre_df = pd.DataFrame(tfidf_genres.toarray())
    genre_df.columns = ['genre' + "_" +
                        genre for genre in tfidf.get_feature_names_out()]
    print(genre_df)

    print("Final Feature Set")
    # Final Feature Set
    all_feature_set = pd.concat([genre_df, ohe_df, model_df], axis=1)

    # Splitting all feature vectors into user song vectors and recommended song vectors
    user_feature_set = all_feature_set.iloc[:len(
        user_all_df)]  # id: user_all_df["spotify_id"]
    # id:  reco_all_df["spotify_id"]
    reco_feature_set = all_feature_set.iloc[len(user_all_df):]

    return user_feature_set, reco_feature_set

def generate_user_summarization_vector(user_feature_set):
    """
    Creates a user profile summarization vector using PCA to capture essential features of user's music preference.
    
    Parameters:
    - user_feature_set: Dataframe containing feature-engineered user songs
    
    Returns:
    A pandas Series representing the user's music taste summarization vector.
    """
    print("Generating User Summarization Vector...")
    print(user_feature_set.head())
    print(user_feature_set.columns)

    optimal_pca = PCA(n_components=len(user_feature_set))
    optimal_pca.fit(user_feature_set)
    user_summarized_vector = pd.Series(optimal_pca.mean_)

    return user_summarized_vector


def generate_final_recommendations(reco_feature_set, user_summarized_vector, reco_all_df):
    """
    Identifies final song recommendations based on cosine similarity between user summarization vector and recommendation feature set.
    
    Parameters:
    - reco_feature_set: Dataframe of feature-engineered recommended songs
    - user_summarized_vector: User profile summarization vector
    - reco_all_df: Dataframe containing metadata of recommended songs
    
    Returns:
    A dataframe of top recommended songs sorted by their similarity to the user profile.
    """
    print("Generating Final Recommendations...")
    print(reco_feature_set[reco_feature_set.isnull().any(axis=1)])
    print(reco_feature_set.head(20))
    reco_feature_set["cos_sim"] = reco_feature_set.apply(lambda reco_vector: cosine_similarity(
        user_summarized_vector.values.reshape(1, -1), reco_vector.values.reshape(1, -1)), axis=1)

    reco_all_df = reco_all_df.reset_index()
    reco_all_df["cos_sim"] = reco_feature_set["cos_sim"].apply(
        lambda sim_2D: sim_2D[0][0]).reset_index().drop(columns="index")

    num_of_reccomendations = 20
    final_recommendations = reco_all_df.sort_values(
        by=['cos_sim'], ascending=False).head(num_of_reccomendations)
    return final_recommendations


def generate_spotify_playlist(username, final_recommendations, spotify_client_id, spotify_client_secret, playlist_create_sp):
    """
    Creates a new Spotify playlist for the user containing the final song recommendations.
    
    Parameters:
    - username: Spotify username of the user
    - final_recommendations: Dataframe containing final song recommendations
    - spotify_client_id: Spotify client ID
    - spotify_client_secret: Spotify client secret
    - playlist_create_sp: Spotipy client instance for creating playlists
    
    Returns:
    URL of the newly created Spotify playlist.
    """
    reco_playlist = playlist_create_sp.user_playlist_create(
        username, "Spotifind's Playlist!", description=f"Generated from Spotifind Recommendation Engine for {username}. Recommendations are based on user's playlists.")
    reco_playlist_id = playlist_create_sp.user_playlists(username)[
        'items'][0]['id']
    added_songs = playlist_create_sp.user_playlist_add_tracks(
        username, reco_playlist_id, tracks=final_recommendations["spotify_id"].values.tolist())
    return playlist_create_sp.user_playlists(username)['items'][0]['external_urls']['spotify']


def recommendation_driver(playlist_ids, sp):
    """
    Main driver function that orchestrates the recommendation process from fetching user data to generating a playlist.
    
    Parameters:
    - playlist_ids: List of user's Spotify playlist IDs
    - sp: Spotipy client instance
    
    Returns:
    URL of the Spotify playlist containing recommendations.
    """
    global username
    global spotify_client_id
    global spotify_client_secret
    print(f"Driver Username: {username}")
    songs_ids, df_meta = generate_user_track_metadata_df(playlist_ids)
    df_features = generate_user_track_audio_features_df(songs_ids)
    user_all_df, user_date_df = generate_user_dfs(df_meta, df_features)
    reco_all_df, reco_date_df = generate_recommendations_dfs(user_all_df)
    user_feature_set, reco_feature_set = feature_engineering(
        user_all_df, reco_all_df, user_date_df, reco_date_df)
    user_summarized_vector = generate_user_summarization_vector(
        user_feature_set)
    final_recommendations = generate_final_recommendations(
        reco_feature_set, user_summarized_vector, reco_all_df)
    return generate_spotify_playlist(username, final_recommendations, spotify_client_id, spotify_client_secret, sp)
