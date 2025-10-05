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

    // Fetch user's saved ideas (jar)
    const token = localStorage.getItem("token");
    let savedIdeas = [];
    if (token) {
      try {
        const resJar = await fetch(`${API_IDEAS}/jar`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (resJar.ok) savedIdeas = await resJar.json();
      } catch (err) {
        console.warn("Could not load user jar:", err);
      }
    }

    ideas.forEach((idea) => {
      if (!idea.lat || !idea.lon) return; // Skip ideas with no coordinates

      const marker = L.marker([idea.lat, idea.lon]).addTo(map);

      // --- Check if idea is already saved ---
      const isSaved = savedIdeas.some((saved) => saved.id === idea.id);
      const buttonHTML = isSaved
        ? `<button class="popup-button" disabled style="opacity:0.7;">💖 Saved</button>`
        : `<button class="popup-button" id="save-btn-${idea.id}">❤️ Save</button>`;

      // --- Popup HTML ---
      const popupHTML = `
        <div class="popup-content">
          <h3 class="popup-title">${idea.title}</h3>
          <p>${idea.note || "No description provided"}</p>
          <p><strong>Categories:</strong> ${idea.categories.join(", ")}</p>
          ${buttonHTML}
        </div>
      `;

      marker.bindPopup(popupHTML);

      // --- Attach click handler when popup opens ---
      marker.on("popupopen", () => {
        const btn = document.getElementById(`save-btn-${idea.id}`);
        if (btn) {
          btn.addEventListener("click", () => toggleSave(idea.id, btn));
        }
      });
    });

    console.log(`Loaded ${ideas.length} public ideas`);
  } catch (err) {
    console.error("Error loading ideas:", err);
  }
}

// --- Save / Heart a public idea ---
async function toggleSave(ideaId, buttonEl) {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in first.");
    return;
  }

  try {
    const res = await fetch(`${API_IDEAS}/heart/${ideaId}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/json",
      },
    });

    const data = await res.json();

    if (res.ok) {
      // Instantly update button state
      buttonEl.textContent = "💖 Saved";
      buttonEl.disabled = true;
      buttonEl.style.opacity = "0.7";
    } else {
      alert(data.detail || "Failed to save idea.");
    }
  } catch (err) {
    console.error("Error saving idea:", err);
    alert("Server error, please try again later.");
  }
}

// --- Run on load ---
loadPublicIdeas();