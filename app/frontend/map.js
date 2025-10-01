// Initialize map centered on Madrid
const map = L.map('map').setView([40.4168, -3.7038], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Example pins (fake data for now)
const pins = [
  { title: "Picnic in the park", coords: [40.4218, -3.7074] },
  { title: "Art gallery date", coords: [40.4158, -3.6994] },
  { title: "Rooftop dinner", coords: [40.4175, -3.7030] }
];

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

// Handle Add button click
document.querySelector(".add-button").addEventListener("click", () => {
  alert("Add new date idea form will go here!");
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


document.querySelector(".home-button").addEventListener("click", () => {
  window.location.href = "home.html";  
});