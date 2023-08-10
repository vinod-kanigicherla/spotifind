import {React, useState} from "react";
import Footer from "../components/Footer";
import Connect from "../components/Connect";
import PlaylistSelect from "../components/PlaylistSelect";
import PlaylistFinal from "../components/PlaylistFinal";
import Authorize from "../components/Authorize";

localStorage.setItem('authorized', 'false');

function Recommend(props) {
    const [loggedIn, setLoggedIn] = useState(false);
    const authorized = localStorage.getItem('authorized') === 'true';
    const [generatingPlaylists, setGeneratingPlaylists] = useState(false);
    const [playlists, setPlaylists] = useState([]);
    const [completedPlaylist, setCompletedPlaylist] = useState("");

    return (
        <div class="relative">
            { (generatingPlaylists && loggedIn) ?
                <PlaylistFinal completedPlaylist={completedPlaylist}/>
            : (loggedIn && (!authorized)) ?
                <Authorize />
            : (loggedIn) ? 
                <PlaylistSelect playlists={playlists} setGeneratingPlaylists={setGeneratingPlaylists} setCompletedPlaylist={setCompletedPlaylist}/> 
            : 
                <Connect setPlaylists={setPlaylists} setLoggedIn={setLoggedIn}/>
            }
            
            <Footer />
        </div>
        
        
    )
}

export default Recommend