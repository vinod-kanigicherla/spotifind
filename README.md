# Spotifind
Spotifind is a comprehensive music recommendation system that harnesses the power of the Spotify API to generate music recommendations based on your favorite playlists. Built with an intuitive interface designed in React and styled with Tailwind CSS, SpotiFind provides a seamless and visually appealing user experience.

> **NOTE - Important Usage Information for Spotifind:**
To enable access to Spotifind, it's necessary for users to have their Spotify account email added to the authorized user list on the Spotify Web API Developer Portal. This step is crucial for fetching the playlists associated with their account. Therefore, individuals interested in utilizing Spotifind must provide their Spotify account email. Please send your account email if you wish to use the application.

---

## Features
- **Playlist Analysis**: Spotifind can analyze any of your Spotify playlists to understand your music preferences.

- **Music Recommendations**: Using data-driven algorithms, SpotiFind suggests songs that match your music taste and habits.

- **Create Custom Playlists**: With a single click, you can create a new Spotify playlist based on the recommendations provided.

---

## Technology Stack
### Frontend

- ReactJS: A robust frontend library used for building user interfaces, making the application reactive and efficient.

- Tailwind CSS: A highly customizable, utility-first CSS framework that is used to style the application and make it responsive and visually appealing.

### Backend

- FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints, powering the recommendation engine.

- Spotify API: Leveraged to fetch user playlists and create new playlists.

## Frontend Usage

With your terminal open in the **frontend** directory, start your React App by running:
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

---

## Backend Usage

### Prerequisites
Before running your FastAPI application, ensure you have the following prerequisites installed:

1. Python: FastAPI requires Python 3.6+.
2. FastAPI: A modern, fast web framework for building APIs with Python 3.6+.
3. Uvicorn: An ASGI server for running your FastAPI application.

With your terminal open in the **backend** project directory, start your FastAPI application by running:
### `python api.py`

---

## Recommendation System Features

1. Our recommendation system, powered by content-based filtering, utilizes the Spotipy API, a lightweight Python library for the Spotify Web API. By leveraging Spotipy, we fetch songs and their attributes from users' playlists using appropriate user credentials. This includes collecting essential metadata such as song names, IDs, playlists, album and artist information, song length, popularity, artist genres, and release dates. Additionally, we gather track audio features such as acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, and time signature. With these attributes, especially genres and release dates, our app conducts a preliminary search for recommended songs that potentially align with the user's music taste.

2. To enable effective content-based recommendations, we perform feature engineering and selection on the user's songs and the recommended songs. This involves techniques such as feature scaling, TFIDF (Term Frequency-Inverse Document Frequency), and one-hot encoding. These transformations convert the relevant song features into appropriate numerical vectors for our content-based filtering model. By representing songs as numeric vectors, we can generate a summarization vector that effectively captures the user's music preferences based on multiple songs in their playlists.

3. Finally, we employ the powerful cosine similarity metric from the Sci-Kit Learn (sklearn) library to compute the similarities between the user's music preference summarization vector (Vector X) and the feature vectors of the recommended songs (Vector Y). The cosine similarity is calculated as the normalized dot product of the two vectors. Using this similarity measure, we identify the songs that are most similar to the user's music taste. These top matches are then curated into a Spotify playlist, providing a personalized and tailored music experience for our users.

---
## App Showcase

![Home](https://github.com/vinod-kanigicherla/spotifind/blob/main/project-pics/Home.png)
   
![How does the app work?](https://github.com/vinod-kanigicherla/spotifind/blob/main/project-pics/Home_How.png)
    
![Authorize](https://github.com/vinod-kanigicherla/spotifind/blob/main/project-pics/Authorize.png)
    
![name](https://github.com/vinod-kanigicherla/spotifind/blob/main/project-pics/PlaylistSelect.png)
    
![name](https://github.com/vinod-kanigicherla/spotifind/blob/main/project-pics/PlaylistSuccess.png)
    
![name](https://github.com/vinod-kanigicherla/spotifind/blob/main/project-pics/Screenshot%202024-03-09%20at%209.42.58%20PM.png)
    

## License
**SpotiFind** is licensed under the MIT License. For more details, see the LICENSE file.

This application is purely educational and not affiliated with Spotify.


