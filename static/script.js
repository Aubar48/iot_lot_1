
document.getElementById('dataForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const sensor = document.getElementById('sensor').value;
    const value = document.getElementById('value').value;

    fetch('/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sensor, value }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message || data.error;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('deleteForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const dataId = document.getElementById('dataId').value;

    fetch(`/data/${dataId}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message || data.error;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('updateForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const id = document.getElementById('updateId').value;
    const sensor = document.getElementById('updateSensor').value;
    const value = document.getElementById('updateValue').value;

    fetch(`/data/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sensor, value }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.message || data.error;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('fetchDataButton').addEventListener('click', function () {
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        const dataDisplay = document.getElementById('dataDisplay');
        dataDisplay.innerHTML = '';
        data.forEach(item => {
            const div = document.createElement('div');
            div.innerText = `ID: ${item.id}, Sensor: ${item.sensor}, Value: ${item.value}, Timestamp: ${item.timestamp}`;
            dataDisplay.appendChild(div);
        });
    })
    .catch(error => console.error('Error:', error));
});
