// Later this will load the "hearted ideas" dynamically from backend.
// For now, just show an alert when removing.
document.querySelectorAll('.remove-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    alert("Removed from your Date Jar!");
  });
});