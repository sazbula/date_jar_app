// Later this will load the "hearted ideas" dynamically from backend.
// For now, just show an alert when removing.
document.querySelectorAll('.remove-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    alert("Removed from your Date Jar!");
  });
});

// Attach Add button functionality to redirect to add.html
const addBtn = document.querySelector(".add-button");

if (addBtn) {
  addBtn.addEventListener("click", () => {
    window.location.href = "add.html"; // redirect to Add page
  });
}