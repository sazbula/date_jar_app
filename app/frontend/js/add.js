// --- API base URL ---
const API_IDEAS = "http://127.0.0.1:8000/api/ideas";

// --- DOM elements ---
const form = document.getElementById("ideaForm");
const catBox = document.getElementById("categoriesList");
const isPublicEl = document.getElementById("isPublic");
const isPrivateEl = document.getElementById("isPrivate");
const pickBtn = document.getElementById("pickLocationBtn");
const mapEl = document.getElementById("map");
const latEl = document.getElementById("lat");
const lonEl = document.getElementById("lon");
const locationSection = document.getElementById("locationSection");

let map, marker;

// ===============================
// 1️⃣ CATEGORY SELECTION (MAX 3)
// ===============================
const categoryCheckboxes = catBox.querySelectorAll('input[type="checkbox"]');

categoryCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const checkedBoxes = Array.from(categoryCheckboxes).filter(cb => cb.checked);

    if (checkedBoxes.length > 3) {
      checkbox.checked = false;
      showCategoryWarning();
    }
  });
});

function showCategoryWarning() {
  let warning = document.querySelector(".category-warning");
  if (!warning) {
    warning = document.createElement("p");
    warning.className = "category-warning";
    warning.textContent = "Sorry, you can only select up to 3!";
    warning.style.color = "#A4161A";
    warning.style.fontSize = "1.5rem";
    warning.style.marginTop = "5px";
    document.querySelector(".categories-label").after(warning);
  }

  warning.style.display = "block";
  setTimeout(() => (warning.style.display = "none"), 2000);
}

// ===================================
// 2️⃣ TOGGLE PUBLIC / PRIVATE CHECKBOX
// ===================================
isPublicEl.addEventListener("change", () => {
  if (isPublicEl.checked) isPrivateEl.checked = false;
});

isPrivateEl.addEventListener("change", () => {
  if (isPrivateEl.checked) isPublicEl.checked = false;
});

// ===========================
// 3️⃣ MAP SETUP (Leaflet)
// ===========================
function initializeMap() {
  if (map) {
    setTimeout(() => map.invalidateSize(), 200);
    return;
  }

  map = L.map("map").setView([40.4168, -3.7038], 12); // Default: Madrid
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);

  // When user clicks on map
  map.on("click", (e) => {
    const { lat, lng } = e.latlng;

    if (!marker) {
      marker = L.marker([lat, lng]).addTo(map);
    } else {
      marker.setLatLng([lat, lng]);
    }

    // Store coordinates
    latEl.value = lat.toFixed(6);
    lonEl.value = lng.toFixed(6);

    console.log(`📍 Selected: ${lat}, ${lng}`);
  });
}

// Show map when “Pick location” clicked
pickBtn.addEventListener("click", () => {
  locationSection.classList.remove("hidden");
  initializeMap();
});

// =================================
// 4️⃣ SUBMIT FORM (SAVE IDEA)
// =================================
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const title = document.getElementById("ideaTitle").value.trim();
  const note = document.getElementById("ideaNote").value.trim();
  const is_public = isPublicEl.checked;
  const categories = Array.from(categoryCheckboxes)
    .filter(cb => cb.checked)
    .map(cb => cb.value);

  if (!title) return alert("Please enter a title.");
  if (categories.length === 0) return alert("Select at least one category.");
  if (categories.length > 3) return alert("You can choose up to 3 categories.");

  const lat = latEl.value ? parseFloat(latEl.value) : null;
  const lon = lonEl.value ? parseFloat(lonEl.value) : null;

  const token = localStorage.getItem("token");
  if (!token) return alert("Please log in first.");

  const payload = {
    title,
    note,
    categories,
    is_public,
    is_home: categories.includes("home"),
    lat,
    lon,
  };

  try {
    const res = await fetch(`${API_IDEAS}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (res.ok) {
      alert("Idea saved successfully!");
      window.location.href = "jar.html";
    } else {
      alert(data.detail || "Failed to save idea.");
    }
  } catch (err) {
    console.error("Error saving idea:", err);
    alert("Server error. Please try again later.");
  }
});