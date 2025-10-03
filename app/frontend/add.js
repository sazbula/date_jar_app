const API_BASE = "http://127.0.0.1:8000/api/ideas";

document.getElementById("ideaForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const idea = {
    title: document.getElementById("ideaTitle").value.trim(),
    note: document.getElementById("ideaNote").value.trim(),
    categories: [document.getElementById("ideaCategory").value], // backend expects list
    address: document.getElementById("ideaAddress").value.trim(),
    is_public: document.getElementById("isPublic").checked,
    lat: document.getElementById("lat").value || null,
    lon: document.getElementById("lon").value || null,
  };

  try {
    const res = await fetch(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(idea),
    });

    const data = await res.json();
    if (res.ok) {
      console.log("✅ Idea saved:", data);
      // redirect to jar page
      window.location.href = "jar.html";
    } else {
      alert("Error: " + (data.detail || "Could not save idea"));
    }
  } catch (err) {
    console.error("❌ Error saving idea:", err);
    alert("Server connection error");
  }
});