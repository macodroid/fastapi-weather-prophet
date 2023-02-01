let actual_temperature = [];
let baseline_temperature = [];
let mlp_temperature = [];
let gru_temperature = [];
let yTime = [];

async function get_data() {
    await get_temperature();
}

// function create_label() {
//     let hours = [];
//     for (let i = 0; i < 24; i++) {
//         let hour = i < 10 ? '0' + i : i;
//         hours.push(hour + ':00');
//     }
//     return hours;
// }

function draw_chart() {
    let contextMLP = document.getElementById('myChart').getContext('2d');

    let chart_settings = {
        type: 'line',
        data: {
            labels: yTime,
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
                },
                {
                    label: "MLP Temperature",
                    backgroundColor: 'rgb(0,0,0)',
                    borderColor: 'rgb(255,249,0)',
                    data: mlp_temperature,
                    fill: false,
                },
                {
                    label: "GRU Temperature",
                    backgroundColor: 'rgb(220,0,0)',
                    borderColor: 'rgb(220,0,0)',
                    data: gru_temperature,
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
    let myChart = new Chart(contextMLP, chart_settings);
}

async function get_temperature() {
    const apiUrl = "https://fastapi-weather-prophet-production.up.railway.app/weather/today";
    // const apiUrl = "http://localhost:8000/weather/today";

    const response = await fetch(apiUrl)
    const weather_data = await response.json()
    console.log(weather_data.result)

    for (let obj of weather_data.result) {
        actual_temperature.push(obj.actual_temperature);
        baseline_temperature.push(obj.temperature_baseline);
        mlp_temperature.push(obj.temperature_mlp);
        gru_temperature.push(obj.temperature_gru)
        yTime.push(obj.weather_date);
    }
}

get_data().then(() => {
    draw_chart()
});

