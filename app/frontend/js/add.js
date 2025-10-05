// api base
const API_IDEAS = "http://127.0.0.1:8000/api/ideas";

// dom elements
const form = document.getElementById("ideaForm");
const catBox = document.getElementById("categoriesList");
const isPublicEl = document.getElementById("isPublic");
const isPrivateEl = document.getElementById("isPrivate");
const pickBtn = document.getElementById("pickLocationBtn");
const latEl = document.getElementById("lat");
const lonEl = document.getElementById("lon");
const locationSection = document.getElementById("locationSection");

let map, marker;

// limit category selection
const categoryCheckboxes = catBox.querySelectorAll('input[type="checkbox"]');
categoryCheckboxes.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const checked = Array.from(categoryCheckboxes).filter(cb => cb.checked);
    if (checked.length > 3) {
      checkbox.checked = false;
      showCategoryWarning();
    }
  });
});

// small warning under categories
function showCategoryWarning() {
  let warning = document.querySelector(".category-warning");
  if (!warning) {
    warning = document.createElement("p");
    warning.className = "category-warning";
    warning.textContent = "you can only select up to 3 categories";
    warning.style.color = "#A4161A";
    warning.style.fontSize = "1.5rem";
    warning.style.marginTop = "5px";
    document.querySelector(".categories-label").after(warning);
  }
  warning.style.display = "block";
  setTimeout(() => (warning.style.display = "none"), 2000);
}

// toggle public/private checkboxes
isPublicEl.addEventListener("change", () => {
  if (isPublicEl.checked) isPrivateEl.checked = false;
});
isPrivateEl.addEventListener("change", () => {
  if (isPrivateEl.checked) isPublicEl.checked = false;
});

// initialize leaflet map
function initializeMap() {
  if (map) {
    setTimeout(() => map.invalidateSize(), 200);
    return;
  }

  map = L.map("map").setView([40.4168, -3.7038], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors"
  }).addTo(map);

  map.on("click", (e) => {
    const { lat, lng } = e.latlng;
    if (!marker) marker = L.marker([lat, lng]).addTo(map);
    else marker.setLatLng([lat, lng]);
    latEl.value = lat.toFixed(6);
    lonEl.value = lng.toFixed(6);
  });
}

// show map when clicking button
pickBtn.addEventListener("click", () => {
  locationSection.classList.remove("hidden");
  initializeMap();
});

// handle form submit
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const title = document.getElementById("ideaTitle").value.trim();
  const note = document.getElementById("ideaNote").value.trim();
  const is_public = isPublicEl.checked;
  const categories = Array.from(categoryCheckboxes)
    .filter(cb => cb.checked)
    .map(cb => cb.value);

  if (!title) return alert("enter a title");
  if (categories.length === 0) return alert("select at least one category");
  if (categories.length > 3) return alert("you can choose up to 3 categories");

  const lat = latEl.value ? parseFloat(latEl.value) : null;
  const lon = lonEl.value ? parseFloat(lonEl.value) : null;
  const token = localStorage.getItem("token");
  if (!token) return alert("please log in first");

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
      alert("idea saved successfully");
      window.location.href = "jar.html";
    } else {
      alert(data.detail || "failed to save idea");
    }
  } catch (err) {
    console.error("error saving idea:", err);
    alert("server error, please try again later");
  }
});