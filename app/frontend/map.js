const res = await fetch("http://127.0.0.1:8000/api/ideas/public");
const publicIdeas = await res.json();

// Initialize map centered on Madrid
const map = L.map('map').setView([40.4168, -3.7038], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

async function loadIdeas() {
  const res = await fetch("http://127.0.0.1:8000/api/ideas");
  const ideas = await res.json();

  ideas.forEach(idea => {
    if (idea.lat && idea.lon) {
      L.marker([idea.lat, idea.lon])
        .addTo(map)
        .bindPopup(`<b>${idea.title}</b><br>${idea.note}`);
    }
  });
}

loadIdeas();

// Add markers for each pin
pins.forEach(pin => {
  L.marker(pin.coords).addTo(map)
    .bindPopup(`
      <div class="popup-content">
        <b class="popup-title">${pin.title}</b><br>
        <button class="popup-button">Add</button>
      </div>
    `);
});



pins.forEach(pin => {
  L.marker(pin.coords).addTo(map)
    .bindPopup(`
      <div class="popup-content">
        <b class="popup-title">${pin.title}</b><br>
        <button class="popup-button"> ❤️Add </button>
      </div>
    `);
});

document.querySelector(".add-button").addEventListener("click", () => {
  window.location.href = "add.html";      
});

document.querySelector(".home-button").addEventListener("click", () => {
  window.location.href = "home.html";  
});

