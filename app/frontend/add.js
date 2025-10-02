document.getElementById("ideaForm").addEventListener("submit", (e) => {
  e.preventDefault();

  const idea = {
    title: document.getElementById("ideaTitle").value,
    note: document.getElementById("ideaNote").value,
    category: document.getElementById("ideaCategory").value,
    isPublic: document.getElementById("isPublic").checked,
    isPrivate: document.getElementById("isPrivate").checked,
  };

  console.log("New Idea Submitted:", idea);

  // Later: send idea to backend
  alert("Idea saved!");
  window.location.href = "map.html";  // go back to map after saving
});