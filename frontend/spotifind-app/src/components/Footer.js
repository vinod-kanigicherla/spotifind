import {React} from "react";

function Footer() {
    return (
        <footer
            class="bg-gray-800 text-center lg:text-left">
                <div class="container p-6 text-neutral-800 dark:text-neutral-200">
                    <div class="grid gap-6 lg:grid-cols-2">
                    <div class="mb-6 md:mb-0">
                        <h5 class="mb-2 font-medium uppercase">ABOUT ME</h5>

                        <p class="mb-4">
                        Hi! I'm Vinod, an incoming student at UCSB majoring in Statistics and Data Science. I am interested in the intersection of data science and computer science, with a particular focus on machine learning and its practical applications for solving real-world challenges.
                        </p>
                    </div>

                    <div class="mb-6 md:mb-0">
                        <h5 class="mb-2 font-medium uppercase">CONTACT ME!</h5>

                        <p class="mb-4">
                        Please feel free to reach out to me via my LinkedIn <a class="underline" target="_blank" href="https://www.linkedin.com/in/vinodkanigicherla/">here</a>  or email at vinod.kanigicherla@gmail.com.
                        </p>
                    </div>
                    </div>
                </div>
            <div
                class="bg-neutral-200 p-4 text-center text-neutral-700 dark:bg-neutral-700 dark:text-neutral-200">
                © 2023 Copyright:
                <a
                class="text-neutral-800 dark:text-neutral-400"
                > Spotifind</a
                >
            </div>
            </footer>
    )
}

export default Footer