async function scan() {
  const username = document.getElementById('username').value;
  document.getElementById('result').innerText = "Scanning...";

  const response = await fetch("https://your-backend.onrender.com/scan", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username })
  });

  const data = await response.json();
  document.getElementById('result').innerText = JSON.stringify(data, null, 2);
}