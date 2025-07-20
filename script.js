const form = document.getElementById("usernameForm");
const resultBox = document.getElementById("resultBox");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value.trim();

  if (!username) return;

  resultBox.innerHTML = "⏳ Scanning @" + username + "...";

  try {
    const res = await fetch("https://gramradar.onrender.com/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username })
    });

    const json = await res.json();
    resultBox.innerHTML = json.is_fake
      ? `❌ @${username} seems like a FAKE account`
      : `✅ @${username} looks REAL!`;
  } catch (err) {
    resultBox.innerHTML = "⚠️ Failed to fetch user data.";
  }
});