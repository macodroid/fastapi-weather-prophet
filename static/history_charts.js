let actual_temperature = [];
let baseline_temperature = [];
let mlp_temperature = [];
let gru_temperature = [];
let yAxes = [];
let btn = document.getElementById('submitBtn');
btn.addEventListener('click', func);
let startDate;
let endDate;


function func() {
    startDate = document.getElementById("startDate").value;
    endDate = document.getElementById("endDate").value;
    get_temperature().then(() => {
        draw_history_chart()
    });
}

async function get_temperature() {
    // const apiUrl = "https://fastapi-weather-prophet-production.up.railway.app/weather/history";
    const apiUrl = "http://localhost:8000/weather/history";
    const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "start_date": startDate,
            "end_date": endDate,
        })
    });
    const weather_history_data = await response.json()
    console.log(weather_history_data.result)

    actual_temperature = [];
    baseline_temperature = [];
    mlp_temperature = [];
    gru_temperature = [];
    yAxes = [];

    for (let obj of weather_history_data.result) {
        actual_temperature.push(obj.actual_temperature);
        baseline_temperature.push(obj.temperature_baseline);
        mlp_temperature.push(obj.temperature_mlp);
        gru_temperature.push(obj.temperature_gru)
        yAxes.push(obj.weather_date)
    }
}

function draw_history_chart() {
    let historyContext = document.getElementById('historyChart').getContext('2d');
    let chartStatus = Chart.getChart("historyChart");
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }
    let history_chart_settings = {
        type: 'line',
        data: {
            labels: yAxes,
            datasets: [
                {
                    label: "Actual Temperature",
                    backgroundColor: 'rgb(146,255,99)',
                    borderColor: 'rgb(146,255,99)',
                    data: actual_temperature,
                    fill: false,
                },
                {
                    label: "Baseline Temperature",
                    backgroundColor: 'rgb(0,33,220)',
                    borderColor: 'rgb(0,33,220)',
                    data: baseline_temperature,
                    fill: false,
                }
            ],
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Real Time Weather Forecast'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day',
                        unitStepSize: 1,
                        displayFormats: {
                            'day': 'MMM DD'
                        }
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    }
    let anotherChart = new Chart(historyContext, history_chart_settings);
    console.log("dasdasdasdasd")
}

