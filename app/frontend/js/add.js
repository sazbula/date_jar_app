const API_BASE = "http://127.0.0.1:8000/api/ideas";

document.getElementById("ideaForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const idea = {
    title: document.getElementById("ideaTitle").value.trim(),
    note: document.getElementById("ideaNote").value.trim(),
    categories: [document.getElementById("ideaCategory").value], // backend expects list
    is_public: document.getElementById("isPublic").checked,
    lat: document.getElementById("lat").value || null,
    lon: document.getElementById("lon").value || null,
  };

  const token = localStorage.getItem("token"); // saved at login

  try {
    const res = await fetch(API_BASE, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`, // ✅ standard JWT header
      },
      body: JSON.stringify(idea),
    });

  let data;
try {
  data = await res.json();
} catch {
  const text = await res.text();
  console.error("Server returned non-JSON:", text);
  alert("Backend crashed: " + text);
  return;
}

    if (res.ok) {
      console.log("✅ Idea saved:", data);
      alert("Idea saved!");
      window.location.href = "jar.html"; // redirect after saving
    } else {
      console.error("❌ Backend error:", data);
      alert("Error: " + (data.detail || "Could not save idea"));
    }
  } catch (err) {
    console.error("❌ Network error:", err);
    alert("Server connection error");
  }
});
console.log("Token being sent:", token);
console.log("Idea being sent:", idea);