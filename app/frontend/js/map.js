// --- API base URL ---
const API_IDEAS = "http://127.0.0.1:8000/api/ideas";

// --- Initialize Leaflet Map ---
const map = L.map("map").setView([40.4168, -3.7038], 12); // Default Madrid center
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

// --- Load all public ideas ---
async function loadPublicIdeas() {
  try {
    const res = await fetch(`${API_IDEAS}/public`);
    if (!res.ok) throw new Error("Failed to load public ideas");

    const ideas = await res.json();

    ideas.forEach((idea) => {
      // Skip ideas with no coordinates
      if (!idea.lat || !idea.lon) return;

      // Create marker
      const marker = L.marker([idea.lat, idea.lon]).addTo(map);

      // Build popup content
      const popupHTML = `
        <div class="popup-content">
          <h3 class="popup-title">${idea.title}</h3>
          <p>${idea.note || "No description"}</p>
          <p><strong>Categories:</strong> ${idea.categories.join(", ")}</p>
          <button class="popup-button" onclick="toggleSave(${idea.id})">
            💖 Save
          </button>
        </div>
      `;

      marker.bindPopup(popupHTML);
    });

    console.log(`✅ Loaded ${ideas.length} public ideas`);

  } catch (err) {
    console.error("❌ Error loading ideas:", err);
  }
}

// --- Save / Heart a public idea ---
async function toggleSave(ideaId) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in first.");
    return;
  }

  try {
    const res = await fetch(`${API_IDEAS}/heart/${ideaId}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`,
        "accept": "application/json",
      },
    });

    const data = await res.json();
    alert(data.message || "Saved!");
  } catch (err) {
    console.error("❌ Error saving idea:", err);
    alert("Server error, please try again.");
  }
}

// --- Run on load ---
loadPublicIdeas();