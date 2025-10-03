// API base URL (update if your backend runs elsewhere)
const API_BASE = "http://127.0.0.1:8000/api/ideas";

// Elements
const ideasList = document.querySelector(".ideas-list");
const categorySelect = document.querySelector(".category-select");

// --- Fetch and render public ideas ---
async function fetchPublicIdeas(category = "") {
  try {
    // Use the correct endpoint for public ideas
    let url = `${API_BASE}/public`;
    // Optionally filter by category if your backend supports it
    if (category) {
      url += `?category=${encodeURIComponent(category)}`;
    }

    const res = await fetch(url);
    const ideas = await res.json();

    // Clear old ideas
    ideasList.innerHTML = "";

    // Render each idea
    ideas.forEach(idea => {
      const item = document.createElement("div");
      item.classList.add("idea-item");

      item.innerHTML = `
        <div>
          <h2 class="idea-title">${idea.title}</h2>
          <p class="idea-note">${idea.note || ""}</p>
        </div>
        <button class="save-btn">❤️ Save</button>
      `;

      // Save button action (adds to your jar)
      const saveBtn = item.querySelector(".save-btn");
      saveBtn.addEventListener("click", () => saveToJar(idea));

      ideasList.appendChild(item);
    });

  } catch (err) {
    console.error("Error loading public ideas:", err);
    ideasList.innerHTML = `<p style="color:red;">Failed to load public ideas.</p>`;
  }
}

// --- Save idea to user's jar ---
async function saveToJar(idea) {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please log in to save ideas.");
      return;
    }

    const res = await fetch(`${API_BASE}/save`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({ idea_id: idea.id })
    });

    if (res.ok) {
      alert("Idea saved to your jar! 🎉");
    } else {
      alert("Failed to save idea.");
    }
  } catch (err) {
    console.error("Error saving idea:", err);
  }
}

// --- Category filter ---
categorySelect.addEventListener("change", () => {
  fetchPublicIdeas(categorySelect.value);
});

// --- Initial load ---
fetchPublicIdeas();