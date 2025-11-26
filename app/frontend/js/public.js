// --- API base URL ---
const API_BASE = "https://date-jar.azurewebsites.net/api/ideas";

// --- DOM elements ---
const ideasList = document.querySelector(".ideas-list");
const categorySelect = document.querySelector(".category-select");

// --- Fetch and render public ideas ---
async function fetchPublicIdeas(category = "") {
  try {
    let url = `${API_BASE}/public`;
    if (category) url += `?category=${encodeURIComponent(category)}`;

    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch ideas.");
    const ideas = await res.json();

    // get user's saved ideas (jar)
    const token = localStorage.getItem("token");
    let savedIdeas = [];
    if (token) {
      const resJar = await fetch(`${API_BASE}/jar`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (resJar.ok) savedIdeas = await resJar.json();
    }

    ideasList.innerHTML = "";

    if (ideas.length === 0) {
      ideasList.innerHTML = `<p>No ideas found in this category.</p>`;
      return;
    }

    // Render each idea
    ideas.forEach((idea) => {
      const item = document.createElement("div");
      item.classList.add("idea-item");

      // check if idea already saved
      const isSaved = savedIdeas.some((saved) => saved.id === idea.id);
      const buttonText = isSaved ? "💖 Saved" : "❤️ Save";
      const buttonDisabled = isSaved ? "disabled" : "";

 item.innerHTML = `
    <div>
      <h2 class="idea-title">${idea.title}</h2>
      <p class="idea-note">${idea.note || ""}</p>
      <p class="idea-categories">
        Categories: ${idea.categories ? idea.categories.join(", ") : "—"}
      </p>
    </div>
    <button class="save-btn" ${buttonDisabled}>${buttonText}</button>
  `;

      const saveBtn = item.querySelector(".save-btn");

      if (!isSaved) {
        saveBtn.addEventListener("click", () =>
          saveToJar(idea.id, saveBtn)
        );
      } else {
        saveBtn.style.opacity = "0.7";
      }

      ideasList.appendChild(item);
    });
  } catch (err) {
    console.error("Error loading public ideas:", err);
    ideasList.innerHTML = `<p style="color:#A4161A;">Failed to load public ideas.</p>`;
  }
}

// --- Save idea to user's jar ---
async function saveToJar(ideaId, buttonEl) {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please log in to save ideas.");
      return;
    }

    const res = await fetch(`${API_BASE}/heart/${ideaId}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();

    if (res.ok) {
      buttonEl.textContent = "💖 Saved";
      buttonEl.disabled = true;
      buttonEl.style.opacity = "0.7";
    } else {
      alert(data.detail || "Failed to save idea.");
    }
  } catch (err) {
    console.error("Error saving idea:", err);
    alert("Server error. Please try again later.");
  }
}


// --- Category filter ---
categorySelect.addEventListener("change", () => {
  fetchPublicIdeas(categorySelect.value);
});

// --- Initial load ---
fetchPublicIdeas();

// --- Add button redirect ---
const addButton = document.querySelector(".add-button");
if (addButton) {
  addButton.addEventListener("click", () => {
    window.location.href = "/add"; 
  });
}