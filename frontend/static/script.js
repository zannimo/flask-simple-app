document.getElementById('myForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const input = document.getElementById('userInput').value;

    const res = await fetch('http://localhost:5001/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userInput: input })
    });

    const data = await res.json();
    document.getElementById('response').textContent = data.message;
});
