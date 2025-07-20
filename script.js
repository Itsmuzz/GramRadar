async function checkProfile() {
  const followers = parseInt(document.getElementById("followers").value);
  const following = parseInt(document.getElementById("following").value);
  const posts = parseInt(document.getElementById("posts").value);
  const avg_likes = parseFloat(document.getElementById("avg_likes").value);
  const avg_comments = parseFloat(document.getElementById("avg_comments").value);
  const bio = document.getElementById("bio").value;
  const has_dp = document.getElementById("has_dp").value.toLowerCase() === "true" ? 1 : 0;

  const payload = {
    followers,
    following,
    posts,
    avg_likes,
    avg_comments,
    bio_length: bio.length,
    has_dp
  };

  try {
    const response = await fetch("https://gramradar.onrender.com/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    document.getElementById("result").innerText = data.result;
  } catch (error) {
    document.getElementById("result").innerText = "❌ Error checking profile.";
    console.error(error);
  }
}