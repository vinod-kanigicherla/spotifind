import axios from "axios";
import {React, useState, useEffect} from "react";
import {CheckBadgeIcon} from '@heroicons/react/24/solid'

const PlaylistFinal = (props) => {

    return (
        <div class = "flex justify-center items-center my-40">
            {
                (props.completedPlaylist !== "") ? (
                    <div class="bg-gray-100">
                        <div class="bg-white p-6  md:mx-auto justify-center">
                            <CheckBadgeIcon class="h-20 w-20 text-indigo-600 ml-56"/>
                            <div class="text-center">
                                <h3 class="md:text-2xl text-base text-gray-900 font-semibold text-center mr-3">Playlist Done!</h3>
                                <p class="text-gray-600 my-1 ">Your playlist has been generated! Click the button below to view it on Spotify.</p>
                                <div class="py-10 text-center  mr-5">
                                    <a href={props.completedPlaylist} target="_blank" class="px-10 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 rounded-lg">
                                        View Playlist
                                </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    ) : 
                    <div class = "flex justify-center items-centers">
                        <div
                            class="h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
                            role="status"
                        >
                        </div>

                        <p class="ml-4 mt-1 block text-md font-semibold text-gray-900">
                                Generating your ideal playlist...
                        </p>
                    </div>
            }
         </div>
    )
}

export default PlaylistFinal