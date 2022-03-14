import { React } from 'react';
import '../Styles/Graph.css';
import visualOne from '../Images/Temperature.png'
import visualTwo from '../Images/TempPredict.png'

function Temperature() {
    return (
        <div className="Main">

            <div className="graph-container">
                <div class="textContainer">
                    <div className="imageText">
                        <h1 class="title graph">Information</h1>
                        <p class="image-description">
                            There are two graphs. The first shows the global temperature changes over time from 1880 to the present.
                            Clearly, the temperature is increasing by a greater amount each year which is a cause for concern. The second graph
                            shows the predictions calculated using time series analysis in machine learning for the global temperature changes up to the year 2050. By the year 2050, the model forecasts 
                            that the world temperature will increase by 1.5 degrees Celsius.
                        </p>
                    </div>
                </div>

                <img className="graphImg" src={visualOne}></img>
                <h3> Temperature <span>Predictions </span></h3>
                <img className="graphImg" src={visualTwo}></img>
            </div>
        </div>
    )
}

export default Temperature;