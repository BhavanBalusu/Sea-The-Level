import { React } from 'react';
import '../Styles/Graph.css';

import carbon from '../Images/carbon.png';
import carbonPredict from '../Images/carbonPredict.png';
import aus from '../Images/Australia.png';
import bra from '../Images/Brazil.png';
import chi from '../Images/China.png';
import ger from '../Images/Germany.png';
import ind from '../Images/India.png';
import jap from '../Images/Japan.png';
import nig from '../Images/Nigeria.png';
import uk from '../Images/UK.png';
import usa from '../Images/USA.png';
import offset from '../Images/carbonOffset.png';


// add other images later

function Carbon() {
    return (
        <div className="Main">

            <div className="graph-container">
                <div class="textContainer">
                    <div className="imageText">
                        <h1 class="title graph">Information</h1>
                        <p class="image-description">
                            The first graph shows the global carbon dioxide emissions over time from 1960 to the present.
                            Just like the temperature, the carbon emissions have surged in recent years which is not sustainable
                            for the world. The next graph contains the predictions for the carbon dioxide emissions up to 2050.
                            By 2050, there will be a forecasted carbon dioxide emissions of 7 metric tons per capita. There are also
                            graphs showing the individual carbon dioxide emissions for 9 major countries.
                        </p>
                    </div>
                </div>

                <img className="graphImg" src={carbon}></img>
                <h3>
                   Carbon <span>Predictions </span>
                </h3>
                <img className="graphImg" src={carbonPredict}></img>
            </div>

           


           <h3>
               Emissions of major countries
           </h3>
            <div className="image-collage">
                <img className="collageImg" src={aus}></img>
                <img className="collageImg" src={bra}></img>
                <img className="collageImg" src={chi}></img>
                <img className="collageImg" src={ger}></img>
                <img className="collageImg" src={ind}></img>
                <img className="collageImg" src={jap}></img>
                <img className="collageImg" src={nig}></img>
                <img className="collageImg" src={uk}></img>
                <img className="collageImg" src={usa}></img>
            </div>

            <div className="graph-container">
                <div class="textContainer">
                    <div className="imageText">
                        <h1 class="title graph">Carbon Offset</h1>
                        <p class="image-description">
                            This bar graph shows how many trees would have to be planted to account for the 
                            emissions of the world and 9 major countries. The United States by far produces the most carbon emissions
                            and is followed by China.
                        </p>
                    </div>
                </div>

                <img className="graphImg3" src={offset}></img>
            </div>

        </div>
    )
}

export default Carbon;