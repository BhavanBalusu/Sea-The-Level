// https://www.kaggle.com/kkhandekar/global-sea-level-1993-2021/code
import React from 'react';
import '../Styles/App.css';
import visual from '../logo.png'
import { Link } from "react-router-dom";

function Home() {

  return (
    <div className="home">
      <div className="home-container">
        <img src={visual} alt="logo" /> {/*graphic TODO: ADD GRAPHIC*/}

      </div>

      <form className="arrow" action="#homeInfo">
        <div>
          <button submit>
            <svg xmlns="http://www.w3.org/2000/svg" width="7vw" height="7vw" fill="currentColor" class="bi bi-arrow-down" viewBox="0 0 16 16">
              <path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z" submit />
            </svg>
          </button>
        </div>
      </form>


      <div class="home-info" id="homeInfo">
        <div className="textBubble">
          <h2>About This Project</h2>
          <p>
            Global warming is a serious issue in our world. In a rapidly changing environment, it is hard to keep track of all of our effects on the world. An example of this is climate change.
            By viewing the trends in the sea levels, carbon dioxide levels, and temperature levels, we can see how much of an impact climate change has on our world. This project provides a visualization of these levels
            and allows you to understand the seriousness of the current issue.
          </p>
        </div>

        <Link to="/Main?#Temperature" class="l">
          <button>Get Started</button>
        </Link>

      </div>
    </div>
  );
}

export default Home;
