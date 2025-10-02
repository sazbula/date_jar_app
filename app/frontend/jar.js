const username = localStorage.getItem("username");
const res = await fetch(`http://127.0.0.1:8000/api/users/${username}/jar`);
const ideas = await res.json();

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