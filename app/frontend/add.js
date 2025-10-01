// Inject + button and modal into every page
const modalHTML = `
  <!-- Floating Add Button -->
  <button class="add-button">+</button>

  <!-- Modal -->
  <div id="ideaModal" class="modal">
    <div class="modal-content">
      <span class="close">&times;</span>
      <h2>Add New Idea</h2>
      <form id="ideaForm">
        <input type="text" id="ideaTitle" placeholder="Title" required>
        <textarea id="ideaNote" placeholder="Note"></textarea>
        <select id="ideaCategory" required>
          <option value="">Choose category</option>
          <option value="Outdoor">Outdoor</option>
          <option value="Indoor">Indoor</option>
          <option value="Romantic">Romantic</option>
          <option value="Food">Food</option>
        </select>
        <label>
          <input type="checkbox" id="isPublic"> Make Public
        </label>
        <button type="submit">Save Idea</button>
      </form>
    </div>
  </div>
`;

// Append modal to the end of body
document.body.insertAdjacentHTML("beforeend", modalHTML);

// Select elements
const modal = document.getElementById("ideaModal");
const addBtn = document.querySelector(".add-button");
const closeBtn = document.querySelector(".close");
const form = document.getElementById("ideaForm");

// Open modal
addBtn.addEventListener("click", () => {
  modal.style.display = "block";
});

// Close modal on ×
closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
});

// Close when clicking outside
window.addEventListener("click", (e) => {
  if (e.target === modal) modal.style.display = "none";
});

// Handle form submission
form.addEventListener("submit", (e) => {
  e.preventDefault();

  const idea = {
    title: document.getElementById("ideaTitle").value,
    note: document.getElementById("ideaNote").value,
    category: document.getElementById("ideaCategory").value,
    isPublic: document.getElementById("isPublic").checked,
    isPrivate: document.getElementById("isPrivate").checked,
  };

  console.log("New Idea Submitted:", idea); // later: send to backend

  modal.style.display = "none";
  form.reset();
});