import React from 'react';
import "../Styles/Main.css"
import Navbar from '../Components/Navbar';
import SeaLevel from '../Components/SeaLevel';
import Temperature from '../Components/Temperature'
import Carbon from '../Components/Carbon'

import seaLevel from '../Images/Figure_1.png'
function Main() {
    return (
        <>
            <Navbar />

            <h1 className="header" id="temp">Temperature Levels</h1>
            <Temperature />
            
            <h1 className="header" id="co">CO<sub>2</sub> Levels</h1>
            <Carbon />

            <h1 class="header" id="sea">Sea Levels</h1>
            <SeaLevel text="lorem" title="Information" img={seaLevel}/>
        </>
    );
}

export default Main;