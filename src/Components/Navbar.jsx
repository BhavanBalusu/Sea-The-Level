import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import {
    Link,
} from "react-router-dom";
import { MdClose, MdNoEncryption } from "react-icons/md"
import { FiMenu } from "react-icons/fi"
import '../Styles/Navbar.css';
import logo from '../logo.png';

const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.navContainer');
    burger.addEventListener('click', () => {
        nav.classList.toggle('nav-active');
    });
}

const Navbar = () => {
    const [navbarOpen, setNavbarOpen] = useState(false);
    const [nav, setNav] = useState(false);
    const [navbarClose] = useState();
    const handleToggle = () => {
        setNavbarOpen(prev => !prev)
    };

    const closeMenu = () => {
        setNavbarOpen(false)
    };

    const changeBackground = () => {
        if (window.scrollY >= 50) {
            setNav(false) // supposed to be true
        } else {
            setNav(false)
        }
    };
    window.addEventListener('scroll', changeBackground)

    return (
        <><div className={nav ? 'nav active' : 'nav'}>
            <div className="navTitle">
                <img src={logo}></img>
            </div>
            <div className="navContainer">
                <Link className="navButton" to="/">
                    Home
                </Link>
                <div className="navButton">
                    <a href="#temp">Temperature Levels</a>
                </div>
                <div className="navButton"> 
                    <a href="#co">CO<sub>2</sub> Levels</a>
                </div>
                <div className="navButton">
                    <a href="#sea">Sea Levels</a>
                </div>
                <Link className="navButton" to="/Predict">
                    Predict
                </Link>
            </div>
            <nav className="navBar">
                <button onClick={handleToggle}>
                    {navbarOpen ? (
                        <MdClose style={{ color: "white", width: "40px", height: "40px", position: "fixed", right: "2vh", top: "2.5vh" }} />
                    ) : (
                        <FiMenu style={{ color: "white", width: "40px", height: "40px", position: "fixed", right: "2vh", top: "2.5vh" }} />
                    )}
                </button>
                <div className={`menuNav ${navbarOpen ? " showMenu" : " closeMenu"}`}>
                    <div className='container1'>
                        <div className="option-container" style={{height: "100vh"}}>
                            <button onClick={handleToggle}>
                                <MdClose style={{ color: "black", width: "40px", height: "40px" }} />
                            </button>
                            <Link className="navB" to="/" onClick={closeMenu}>
                                Home
                            </Link>
                            <a href="#temp" className="navB" onClick={closeMenu}>
                                Temperature Levels
                            </a>
                            <a href="#co" className="navB" onClick={closeMenu}>
                                CO<sub>2</sub> Levels
                            </a>
                            <a href="#sea" className="navB" onClick={closeMenu}>
                                Sea Levels
                            </a>
                            <Link className="navB" to="/Predict">
                                Predict
                            </Link>
                        </div>
                        <div  className='container2'>
                        </div>
                    </div>
                </div>
            </nav>
            <div>
            </div>

        </div >
        </>
    );
};

export default Navbar;