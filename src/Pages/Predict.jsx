import React, {useState, useRef} from 'react';
import Navbar from '../Components/NavBarPredict.jsx'
import predictCo2 from './predictCo2.csv';
import predictTemp from './predictTemp.csv';
import '../Styles/Predict.css'

function Predict() {

    let tempYear = useRef("");
    let tempMonth = useRef("");

    let coYear = useRef();
    let coMonth = useRef();

    const [tempRes, setTempRes] = useState("");
    const [coRes, setCoRes] = useState("");

    function submitTemp(e) {
        e.preventDefault();
        if (tempYear.current.value === "" || tempMonth.current.value === "") return;
        if (parseInt(tempMonth.current.value) > 12 || parseInt(tempMonth.current.value) < 1) return false;
        if (parseInt(tempYear.current.value) > 2100 || parseInt(tempYear.current.value) < 2022) return false;
        setDataTemp();
        console.log(tempRes);
        // call function to find value
    }

    function submitCo(e) {
        e.preventDefault();
        if (coYear.current.value === "" || coMonth.current.value === "") return;
        if (parseInt(coMonth.current.value) > 12 || parseInt(coMonth.current.value) < 1) return false;
        if (parseInt(coYear.current.value) > 2100 || parseInt(coYear.current.value) < 2022) return false;
        setDataCO();
        // call function to find value
        console.log(coRes);
    }

    async function setDataTemp(){
        const response = await fetch(predictTemp);
        const data = await response.text();
        const rows = data.split('\n')
        const row = rows[(parseInt(tempYear.current.value) - 2022) * 12 + parseInt(tempMonth.current.value) - 1].split(',');
        console.log(row[1]);
        setTempRes(row[1]);
    }

    async function setDataCO() {

        const response = await fetch(predictCo2);
        const data = await response.text();
        const rows = data.split('\n')
        const row = rows[(parseInt(coYear.current.value) - 2022) * 12 + parseInt(coMonth.current.value) - 1].split(',');
        setCoRes(row[1]);
    }


    return (
        <>
            <Navbar />
            <h1 className="predict-title">Predict Future Values</h1>
            <div class="wrapper temp">
                <div className="inputs temp">
                    <h2 className="subtitle">Predict Future Temperature Value</h2>
                    <form onSubmit={submitTemp}>
                        <input ref={tempYear} class="year" type="number" placeholder={"Year (2022-2100)"} required />
                    </form>

                    <form onSubmit={submitTemp}>
                        <input ref={tempMonth} class="month" type="number" placeholder="Month (1-12)" required />
                    </form>
                </div>

                <div className="results temp">
                    <h3>Temperature Result (° Celsius): </h3><h4>{tempRes}</h4>
                </div>

            </div>
            
            <div className="wrapper co">
                <div className="inputs co">
                    <h2 className="subtitle">Predict Future CO<sub>2</sub> Value</h2>
                    <form onSubmit={submitCo}>
                        <input ref={coYear} class="year" type="number" placeholder={"Year (2022-2100)"} required /> {/* 2023 - 2100 */}

                    </form>

                    <form onSubmit={submitCo}>
                        <input ref={coMonth} class="month" type="number" placeholder="Month (1-12)" required />
                    </form>
                </div>

                <div className="results co">
                    <h3>CO<sub>2</sub> Result (Metric tons per capita): </h3><h4>{coRes}</h4>
                </div>
            </div>
        </>
    )
}

export default Predict;
