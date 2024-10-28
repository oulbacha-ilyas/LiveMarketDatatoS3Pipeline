document.getElementById('start-streaming-btn').addEventListener('click', function() {
    fetch('/start_streaming', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response-message').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').innerText = 'An error occurred.';
        });
});

document.getElementById('stop-streaming-btn').addEventListener('click', function() {
    fetch('/stop_streaming', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response-message').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').innerText = 'An error occurred.';
        });
});

document.getElementById('save-to-bucket-btn').addEventListener('click', function() {
    // You need to specify the timeframe, or modify the backend to handle this
    const timeframe = '1min';  // Replace with the actual timeframe
    fetch('/save_to_bucket', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ timeframe: timeframe })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response-message').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').innerText = 'An error occurred.';
        });
});

document.getElementById('reset-df-btn').addEventListener('click', function() {
    // You need to specify the timeframe, or modify the backend to handle this
    const timeframe = '1min';  // Replace with the actual timeframe
    fetch('/reset_df', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ timeframe: timeframe })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('response-message').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('response-message').innerText = 'An error occurred.';
        });
});
