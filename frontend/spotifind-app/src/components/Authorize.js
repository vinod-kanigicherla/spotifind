import axios from "axios";
import React from "react";
import { NavLink } from "react-router-dom";

const Authorize = (props) => {
    const authorizeSubmit = async (event) => {
        const authorize = async () => {
            try {
              const response = await axios.get('/authorize/');
              // This will redirect the user to the Spotify authorization page
              window.location.href = response.data.auth_url;
            } catch (e) {
              console.error(e);
            }
          };
          
        authorize();
    }

    return (
        <div class="flex items-center justify-center static left-0 my-20">
            <div class="w-full rounded-md bg-white shadow dark:border sm:max-w-lg xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
                    <form
                        onSubmit={authorizeSubmit}
                        >
                        <div>
                            <label class="block mb-2 text-xl font-bold text-gray-900 dark:text-white">Authorize your Spotify Account...</label>
                            <p class="block mb-5 text-sm font-medium text-gray-900 dark:text-white">Looks like your Spotifind hasn't connected to your spotify. Click the button below to authorize spotify to access your playlists: </p>
                            <input type="submit"
                                className="mb-2 rounded-md bg-cyan-800 px-3.5 py-2.5 text-sm hover:bg-cyan-600 font-semibold text-white shadow-sm"
                                value="Authorize"
                            >
                            </input>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Authorize