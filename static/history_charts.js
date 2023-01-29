var btn = document.getElementById('submitBtn');
btn.addEventListener('click', func);
let startDate;
let endDate;

function func() {
    startDate = document.getElementById("startDate").value;
    endDate = document.getElementById("endDate").value;
}

async function get_temperature() {
    // const apiUrl = "https://fastapi-weather-prophet-production.up.railway.app/weather/today";
    const apiUrl = "http://localhost:8000/weather/today";

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