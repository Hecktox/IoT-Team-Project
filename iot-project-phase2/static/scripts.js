// Function to update temperature and humidity display
function updateTemperatureHumidity() {
    fetch('/temp_humidity')
    .then(response => response.json())
    .then(data => {
        // Check if the data contains temperature and humidity
        if(data.temperature && data.humidity) {
            document.getElementById('temperature').innerText = `Temperature: ${data.temperature} °C`;
            document.getElementById('humidity').innerText = `Humidity: ${data.humidity} %`;
        } else {
            console.error('Temperature and humidity data are not available');
        }
    })
    .catch(error => console.error('Error fetching temperature and humidity:', error));
}

// Function to update fan status display
function updateFanStatus() {
    fetch('/fan_status')
    .then(response => response.json())
    .then(data => {
        // Check if the data contains fan status
        if(data.fan_status) {
            document.getElementById('fan-status').innerText = `Fan Status: ${data.fan_status}`;
        } else {
            console.error('Fan status data is not available');
        }
    })
    .catch(error => console.error('Error fetching fan status:', error));
}

// Call these functions on a set interval if you want them to auto-update
setInterval(updateTemperatureHumidity, 5000); // every 5 seconds
setInterval(updateFanStatus, 5000); // every 5 seconds

// Trigger the updates immediately on page load as well
updateTemperatureHumidity();
updateFanStatus();
