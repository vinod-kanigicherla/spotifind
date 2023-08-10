import {useState, React} from "react";
import { Disclosure, Menu, Transition } from '@headlessui/react'
import { Router, NavLink } from 'react-router-dom'
import logo from "../logo.svg"
    
const nav = [
    {name: "Home", href: "/"},
    {name: "Recommend!", href: "/recommend"},
]

function Navbar() {
    const [currPage, setCurrPage] = useState("Home");

    return (
        <Disclosure as="nav" className="bg-gray-800">
                {({ open }) => (
                <>
                    <div className="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                        <div class="flex flex-shrink-0 items-center pr-10 pl-8">
                            <NavLink 
                                className = "text-white font-bold text-2xl"
                                to = "/"
                                >
                                    Spotifind
                            </NavLink>
                        </div>
                        <div className="flex space-x-4">
                            {
                                nav.map((page) => (
                                    <NavLink
                                        key={page.name}
                                        to={page.href}
                                        className={({ isActive, isPending }) => isActive ? "text-white bg-gray-900 rounded-md px-4 py-5 self-center text-sm" : "text-gray-300 hover:bg-gray-700 hover:text-white rounded-md px-4 py-5 text-sm"}
                                    >
                                        {page.name}
                                    </NavLink>
                                ))
                                
                            }
                        </div>
                    </div>
                </>
                )}
        </Disclosure>

    )
}

export default Navbar