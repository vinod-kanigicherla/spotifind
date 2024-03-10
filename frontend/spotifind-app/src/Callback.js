import React, { useEffect } from "react";
import axios from "axios";
import { NavLink, useLocation } from "react-router-dom";

function Callback(props) {
  const location = useLocation();

  useEffect(() => {
    const getAccessToken = async () => {
      // Parse the authorization code from the URL
      const code = new URLSearchParams(location.search).get("code");

      try {
        // Send the code to the backend
        const response = await axios.get(`/callback?code=${code}`);

        console.log(response);
        console.log(response.data.message);
        if (
          response.data.message ===
          "Authorization successful. You can now use Spotipy to make authenticated API requests."
        ) {
          localStorage.setItem("authorized", "true");
        }
        props.setAuthorized(true);
      } catch (e) {
        console.error(e);
      }
    };
    getAccessToken();
  }, [location]);

  return (
    <div class="flex items-center justify-center h-screen">
      <div class="w-full rounded-md bg-white shadow dark:border sm:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700 mb-40">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <form class="space-y-4 md:space-y-6">
            <div>
              <label class="block mb-2 text-xl font-bold text-green-500 dark:text-white">
                You've been authorized!
              </label>
              <p class="block mb-5 text-sm font-medium text-green-500 dark:text-white">
                Spotifind is now connected to your spotify account. Click the
                button below to proceed to log back in to select your playlists:
              </p>
              <NavLink
                className="mt-3 rounded-md bg-gray-600 px-3.5 py-2.5 text-sm hover:bg-gray-500 font-semibold text-white shadow-sm"
                to="/recommend"
              >
                Log In
              </NavLink>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Callback;
