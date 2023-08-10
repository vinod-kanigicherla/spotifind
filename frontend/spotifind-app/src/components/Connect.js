import React, { useEffect, useState } from "react";
import axios from "axios";
import { NavLink } from "react-router-dom";

function Connect(props) {
    const [username, setUsername] = useState("")
    const [tryAgain, setTryAgain] = useState(false)

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const response = await axios.post("/submit_username/", {
                username: username,
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (response.data.message.includes("Invalid")) {
                setTryAgain(true)
            }
            // Add Invalid (if invalid in response.data.playlists, set error show true ) 
            // https://v1.tailwindcss.com/components/alerts
            if (response.data.playlists) {
                props.setPlaylists(response.data.playlists);
                props.setLoggedIn(true)
            }
        } catch (e) {
            console.error(e)
        }
    }

    return (
        <div>
            <div class="bg-indigo-900 text-center py-4 lg:px-4 top-10">
                <div class="p-2 bg-indigo-800 items-center text-indigo-100 leading-none lg:rounded-full flex lg:inline-flex" role="alert">
                    <span class="flex rounded-full bg-indigo-500 uppercase px-2 py-1 text-xs font-bold mr-3">NOTE</span>
                    <span class="font-semibold mr-2 text-left flex-auto">You will be prompted by Spotify to allow us to access your playlists. </span>
                </div>
            </div>
            {tryAgain ? (<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded flex justify-center" role="alert">
                <strong class="font-bold">Invalid Username!</strong>
                <span class="block sm:inline"> Try Again.</span>
            </div>) : <br/>}
        <div class="flex items-center justify-center h-screen">
            <div class="w-full rounded-md bg-white shadow dark:border sm:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700 mb-60">
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <form 
                        class="space-y-4 md:space-y-6" 
                        onSubmit={handleSubmit}
                        >
                        <div>
                            <label class="block mb-2 text-xl font-bold text-gray-900 dark:text-white">Connect to Spotify</label>
                            <p class="block mb-5 text-sm font-medium text-gray-900 dark:text-white">To begin, enter your Spotify Username below to fetch your playlists:</p>
                            <input type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)} class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Spotify Username" required=""/>
                            <input type="submit"
                                    className="mt-3 rounded-md bg-gray-500 px-3.5 py-2.5 text-sm hover:bg-gray-600 font-semibold text-white shadow-sm"
                                    value="Submit"
                            >
                            </input>
                        </div>
                    </form>
                </div>
                
            </div>
        </div>
        </div>
    )
}

export default Connect