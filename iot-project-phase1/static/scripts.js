document.getElementById('switchButton').addEventListener('click', function() {
    toggleLED();
});

document.getElementById('holdSwitch').addEventListener('mousedown', function() {
    holdLED('ON');
});

document.getElementById('holdSwitch').addEventListener('mouseup', function() {
    holdLED('OFF');
});

let flashingInterval;
let isFlashing = false;
document.getElementById('flashingToggleSwitch').addEventListener('click', function() {
    if (!isFlashing) {
        flashingInterval = setInterval(function() {
            toggleFlashingLED();
        }, 1000);  // Flash every 1 second
        isFlashing = true;
    } else {
        clearInterval(flashingInterval);
        flashingInterval = null;
        isFlashing = false;
        updateSwitchStatus('flashingToggleSwitch', 'OFF');
    }
});

function toggleLED() {
    const ledIcon = document.getElementById('ledIcon');
    let switchStatus = document.getElementById('switchStatus').innerText;
    let newStatus = switchStatus === 'OFF' ? 'ON' : 'OFF';

    fetch('/toggle', {
        method: 'POST',
        body: new URLSearchParams({ switch_status: switchStatus }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        ledIcon.src = `/static/images/led_${data.status.toLowerCase()}.png`;
        document.getElementById('switchStatus').innerText = data.status;
    });
}

function holdLED(status) {
    fetch('/hold', {
        method: 'POST',
        body: new URLSearchParams({ switch_status: status }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        const ledIcon = document.getElementById('ledIcon');
        ledIcon.src = `/static/images/led_${data.status.toLowerCase()}.png`;
        document.getElementById('switchStatus').innerText = data.status;
    });
}

function toggleFlashingLED() {
    const ledIcon = document.getElementById('ledIcon');
    let switchStatus = document.getElementById('switchStatus').innerText;

    fetch('/flashing', {
        method: 'POST',
        body: new URLSearchParams({ switch_status: switchStatus }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        ledIcon.src = `/static/images/led_${data.status.toLowerCase()}.png`;
        document.getElementById('switchStatus').innerText = data.status;
    });
}

function updateSwitchStatus(switchId, status) {
    const ledIcon = document.getElementById('ledIcon');
    fetch(`/${switchId}`, {
        method: 'POST',
        body: new URLSearchParams({ switch_status: status }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        ledIcon.src = `/static/images/led_${data.status.toLowerCase()}.png`;
        document.getElementById('switchStatus').innerText = data.status;
    });
}
