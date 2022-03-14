import { React } from 'react';
import '../Styles/Graph.css';

function Graph(props) {
    return (
        <div className="Main">
            
            <div className="graph-container">
                <div class="textContainer">
                    <div className="imageText">
                        <h1 class="title graph">{props.title}</h1>
                        <p class="image-description">
                            This final section has a graph showing the variations in sea levels over time. The sea levels
                            are trending dangerously upwards as was the case with the temperature and carbon dioxide
                            levels.
                        </p>
                    </div>
                </div>

                <img className ="graphImg" src={props.img}></img>
            </div>
        </div>
    )
}

export default Graph;