import React from "react";
import home1 from '../home1.jpg'
import {CloudIcon, WrenchIcon, CodeBracketIcon} from '@heroicons/react/24/solid'
import { NavLink } from "react-router-dom";
import Footer from "../components/Footer";

function Home() {
    return (
        <div className="overflow-hidden bg-white py-20 sm:py-10">
            <div className="mx-auto max-w-2xl py-32 sm:py-14 lg:py-30">
                <div className="hidden sm:mb-8 sm:flex sm:justify-center">
                    <div className="text-center">
                        <h2 className="text-lg font-semibold leading-7 text-violet-600">Want to discover your perfect playlist match? </h2>
                        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                        Spotifind has got you covered!
                        </h1>
                        <p className="mt-6 text-lg leading-8 text-gray-600">
                        Discover new music like never before with your favorite playlists! Our smart recommendation system takes the playlists you love and opens doors to an exciting musical journey. Just pick your favorite playlists, and watch as our engine creates a special mix of songs you've never heard. Click the button below to get started!
                        </p>
                        <div className="mt-10 flex items-center justify-center gap-x-6">
                            <NavLink
                                to="/recommend"
                                className="rounded-md bg-violet-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                            >
                                Get Started
                            </NavLink>
                        </div>
                    </div>
                </div>
            </div>  

            <div className="bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] w-full h-auto lg:px-8 py-10 sm:justify-center">
                <p className="mt-1 ml-6 mb-10 text-3xl font-bold text-indigo-900 sm:text-4xl">How does it work?</p>
                <div className="grid max-w-2xl grid-cols-3 gap-x-8 gap-y-16 sm:gap-y-20 lg:mx-0 lg:max-w-none">
                    <div className="mt-4">
                        <CloudIcon className="h-20 w-20 ml-36 mb-4 text-indigo-600"/>
                        <p className="text-md ml-7 text-indigo-900"> Our recommendation system, powered by content-based filtering, utilizes the Spotipy API, a lightweight Python library for the Spotify Web API. By leveraging Spotipy, we fetch songs and their attributes from users' playlists using appropriate user credentials. This includes collecting essential metadata such as song names, IDs, playlists, album and artist information, song length, popularity, artist genres, and release dates. Additionally, we gather track audio features such as acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, and time signature. With these attributes, especially genres and release dates, our app conducts a preliminary search for recommended songs that potentially align with the user's music taste. </p>
                    </div>
                    <div className="mt-4">
                        <CodeBracketIcon className="h-20 w-20 ml-36 mb-4 text-indigo-600"/>
                        <p className="text-md ml-4 text-indigo-900"> To enable effective content-based recommendations, we perform feature engineering and selection on the user's songs and the recommended songs. This involves techniques such as feature scaling, TFIDF (Term Frequency-Inverse Document Frequency), and one-hot encoding. These transformations convert the relevant song features into appropriate numerical vectors for our content-based filtering model. By representing songs as numeric vectors, we can generate a summarization vector that effectively captures the user's music preferences based on multiple songs in their playlists. </p>
                    </div>
                    <div className="mt-4">
                        <WrenchIcon className="h-20 w-20 ml-36 mb-4 text-indigo-600"/>
                        <p className="text-md ml-4 text-indigo-900"> Finally, we employ the powerful cosine similarity metric from the Sci-Kit Learn (sklearn) library to compute the similarities between the user's music preference summarization vector (Vector X) and the feature vectors of the recommended songs (Vector Y). The cosine similarity is calculated as the normalized dot product of the two vectors. Using this similarity measure, we identify the songs that are most similar to the user's music taste. These top matches are then curated into a Spotify playlist, providing a personalized and tailored music experience for our users. </p>
                    </div>

                    
                    {/* <div>
                        <img
                            src={home1}
                            alt="Product screenshot"
                            className="h-[22rem] w-[23rem] rounded-xl shadow-xl ring-1 ring-gray-400/10 sm:w-[32rem] md:-ml-4 lg:-ml-0 border-4 mt-24 border-violet-600"
                        />
                        <img
                            src={home1}
                            alt="Product screenshot"
                            className="h-[22rem] w-[23rem] rounded-xl shadow-xl ring-1 ring-gray-400/10 sm:w-[32rem] md:-ml-4 lg:-ml-0 border-4 mt-3 border-violet-600"
                        />
                        <img
                            src={home1}
                            alt="Product screenshot"
                            className="h-[22rem] w-[23rem] rounded-xl shadow-xl ring-1 ring-gray-400/10 sm:w-[32rem] md:-ml-4 lg:-ml-0 border-4 mt-3 border-violet-600"
                        /> 
                    </div> */}
                </div>
            </div>  
            <Footer />
        </div>
    )
}

export default Home 