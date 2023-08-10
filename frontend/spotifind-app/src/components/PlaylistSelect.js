import axios from "axios";
import {React, useState, useEffect} from "react";

function PlaylistSelect(props) {

    // Loading Playlists
    const [playlistNames, playlistIds, playlistImages] = props.playlists
    const generatePlaylists = (playlistNames) => {
        let content = []
        for (let i in playlistNames) {
            content.push(
                <div class="flex items-center pl-4 border border-gray-200 rounded dark:border-gray-700 w-auto mt-2">
                    <img src={playlistImages[i]}  width="60" height="60" class="mr-3"/>
                    <input 
                        id="bordered-checkbox" 
                        type="checkbox" 
                        value={playlistNames[i]} 
                        name={playlistNames[i]}
                        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                        onChange={() => handleOnChange(i)}
                    
                    />
                    <label for="bordered-checkbox-1" class="w-full py-4 ml-2 text-sm font-medium text-gray-900 dark:text-gray-300">{playlistNames[i]}</label>
                </div>
            )
        }
        return content

    }
    
    //Selecting Playlists
    const [selectedPlaylists, setSelectedPlaylists] = useState(
        new Array(playlistIds.length).fill(false)
    )
    const [selectedPlaylistIds, setSelectedPlaylistIds] = useState(playlistNames)

    const handleOnChange = (idx) => {
        const updatedSelectedPlaylists = selectedPlaylists.map((state, map_idx) => 
            idx == map_idx ? !state : state
        );
        setSelectedPlaylists(updatedSelectedPlaylists)
    }

    // Called EVERYTIME React State Above Updates
    useEffect(() => {
        const updatedselectedPlaylistIds = playlistIds.filter((name, name_idx) => 
            selectedPlaylists[name_idx]
        );
        setSelectedPlaylistIds(updatedselectedPlaylistIds);
    }, [selectedPlaylists]);


    // Handle Submit Function Here
    const handleSubmit = async (event) => {
        event.preventDefault();
        
        if (localStorage.getItem('authorized') === 'true') {
            try {
                props.setGeneratingPlaylists(true);
                const response = await axios.post("/submit_playlists/", {
                    playlistIds: selectedPlaylistIds
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                props.setCompletedPlaylist(response.data.reco_playlists_link)
            } catch (e) {
                console.error(e)
            }
        }
    }
    return (
    <div class="relative">
    <div class="flex items-center justify-center static left-0 my-10">
        <div class="w-full rounded-md bg-white shadow dark:border sm:max-w-lg xl:p-0 dark:bg-gray-800 dark:border-gray-700">
                <label class="block mx-5 mt-5 text-md font-bold text-gray-900 dark:text-white">Select Your Playlists For Our Recommendation Engine:</label>
                <div class="mx-5 my-5">
                        <form 
                            onSubmit={handleSubmit}
                        >
                            {generatePlaylists(playlistNames)}
                            <input type="submit"
                                    className="my-5 rounded-md bg-gray-500 px-3.5 py-2.5 text-sm hover:bg-gray-600 font-semibold text-white shadow-sm"
                                    value="Recommend!"
                                >
                            </input>
                        </form>  
                </div>
        </div>
    </div>
    </div>
    )
}

export default PlaylistSelect