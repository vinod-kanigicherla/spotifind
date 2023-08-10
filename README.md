# spotifind
Spotifind is a comprehensive music recommendation system that harnesses the power of the Spotify API to generate music recommendations based on your favorite playlists. Built with an intuitive interface designed in React and styled with Tailwind CSS, SpotiFind provides a seamless and visually appealing user experience.

## Features
- Playlist Analysis: SpotiFind can analyze any of your Spotify playlists to understand your music preferences.

- Music Recommendations: Using data-driven algorithms, SpotiFind suggests songs that match your music taste and habits.

- Create Custom Playlists: With a single click, you can create a new Spotify playlist based on the recommendations provided.

## Technology Stack
### Frontend

- ReactJS: A robust frontend library used for building user interfaces, making the application reactive and efficient.

- Tailwind CSS: A highly customizable, utility-first CSS framework that is used to style the application and make it responsive and visually appealing.

### Backend

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints, powering the recommendation engine.

- Spotify API: Leveraged to fetch user playlists and create new playlists.

## Recommendation System Features

1. Our recommendation system, powered by content-based filtering, utilizes the Spotipy API, a lightweight Python library for the Spotify Web API. By leveraging Spotipy, we fetch songs and their attributes from users' playlists using appropriate user credentials. This includes collecting essential metadata such as song names, IDs, playlists, album and artist information, song length, popularity, artist genres, and release dates. Additionally, we gather track audio features such as acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, and time signature. With these attributes, especially genres and release dates, our app conducts a preliminary search for recommended songs that potentially align with the user's music taste.

2. To enable effective content-based recommendations, we perform feature engineering and selection on the user's songs and the recommended songs. This involves techniques such as feature scaling, TFIDF (Term Frequency-Inverse Document Frequency), and one-hot encoding. These transformations convert the relevant song features into appropriate numerical vectors for our content-based filtering model. By representing songs as numeric vectors, we can generate a summarization vector that effectively captures the user's music preferences based on multiple songs in their playlists.

3. Finally, we employ the powerful cosine similarity metric from the Sci-Kit Learn (sklearn) library to compute the similarities between the user's music preference summarization vector (Vector X) and the feature vectors of the recommended songs (Vector Y). The cosine similarity is calculated as the normalized dot product of the two vectors. Using this similarity measure, we identify the songs that are most similar to the user's music taste. These top matches are then curated into a Spotify playlist, providing a personalized and tailored music experience for our users.

## License
**SpotiFind** is licensed under the MIT License. For more details, see the LICENSE file.

This application is purely educational and not affiliated with Spotify.


