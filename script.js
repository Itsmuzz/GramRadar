const form = document.getElementById("scanForm");
const resultBox = document.getElementById("resultBox");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(form);
  const data = {};
  formData.forEach((val, key) => {
    data[key] = isNaN(val) ? val : parseFloat(val);
  });

  resultBox.innerHTML = "⏳ Scanning...";

  try {
    const res = await fetch("https://gramradar.onrender.com/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const json = await res.json();
    resultBox.innerHTML = json.is_fake
      ? "<span class='fake'>❌ Fake Account Detected</span>"
      : "<span class='real'>✅ Real Account Detected</span>";
  } catch (err) {
    resultBox.innerHTML = "⚠️ Error: Unable to contact AI server.";
    console.error(err);
  }
});