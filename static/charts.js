let actual_temperature = [];
let baseline_temperature = [];
let mlp_temperature = [];
let gru_temperature = [];

async function get_data() {
    await get_temperature();
}

function create_label() {
    let hours = [];
    for (let i = 0; i < 24; i++) {
        let hour = i < 10 ? '0' + i : i;
        hours.push(hour + ':00');
    }
    return hours;
}

function draw_chart() {
    const contextMLP = document.getElementById('myChart').getContext('2d');

    let chart_settings = {
        type: 'line',
        data: {
            labels: create_label(),
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
    let myChart = new Chart(contextMLP, chart_settings);

    const source = new EventSource("/temperature-data");

    source.onmessage = function (event) {
        const data = JSON.parse(event.data);

        chart_settings.data.datasets[0].data.push(data['actual_temperature']);
        chart_settings.data.datasets[1].data.push(data['baseline_temperature']);
        myChart.update();
    }
}

async function get_temperature() {
    const apiUrl = "http://127.0.01:8000/weather/today"

    const response = await fetch(apiUrl)
    const weather_data = await response.json()
    console.log(weather_data.result)

    for (let obj of weather_data.result) {
        actual_temperature.push(obj.actual_temperature);
        baseline_temperature.push(obj.temperature_baseline);
        mlp_temperature.push(obj.temperature_mlp);
        gru_temperature.push(obj.temperature_gru);
    }
}


get_data().then(() => {
    draw_chart()
});
