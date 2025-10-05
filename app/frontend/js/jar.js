const API_IDEAS = "http://127.0.0.1:8000/api/ideas";

// Load ideas from your jar
async function loadMyJar() {
  const token = localStorage.getItem("token");
  if (!token) {
    alert("Please log in first.");
    return;
  }

  try {
    const res = await fetch(`${API_IDEAS}/jar`, {
      headers: {
        "Authorization": `Bearer ${token}`,
        "accept": "application/json",
      },
    });

    if (!res.ok) throw new Error("Failed to load your jar.");

    let ideas = await res.json();

    //  Apply category filter (frontend side)
    const selectedCategory = document.querySelector("#categorySelect").value;
    if (selectedCategory) {
      ideas = ideas.filter((idea) => idea.categories.includes(selectedCategory));
    }

    const list = document.querySelector(".ideas-list");
    list.innerHTML = "";

    if (ideas.length === 0) {
      list.innerHTML = `<p style="color:#A4161A; text-align:center;">No ideas in this category.</p>`;
      return;
    }

    ideas.forEach((idea) => {
      const item = document.createElement("div");
      item.className = "idea-item";
      item.innerHTML = `
        <div class="idea-text">
          <h2 class="idea-title">${idea.title}</h2>
          <p class="idea-note">${idea.note || ""}</p>
          <p><em>Categories:</em> ${idea.categories.join(", ")}</p>
        </div>
        <button class="btn remove-btn" data-id="${idea.id}">Remove</button>
      `;
      list.appendChild(item);
    });

    // Add "Remove" handlers
    document.querySelectorAll(".remove-btn").forEach(btn => {
      btn.addEventListener("click", async () => {
        const ideaId = btn.dataset.id;
        await removeFromJar(ideaId);
      });
    });

  } catch (err) {
    console.error(err);
    alert("Error loading ideas.");
  }
}

// Remove idea from jar (works for both own & hearted)
async function removeFromJar(ideaId) {
  const token = localStorage.getItem("token");

  try {
    const res = await fetch(`${API_IDEAS}/heart/${ideaId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
        "accept": "application/json",
      },
    });

    const data = await res.json();

    if (res.ok) {
      const msg = data.message || "Removed from your jar!";
      alert(msg);

      const item = document.querySelector(`.remove-btn[data-id='${ideaId}']`)?.closest(".idea-item");
      if (item) item.remove();

      // reload filtered view
      setTimeout(loadMyJar, 300);
    } else {
      alert(data.detail || "Failed to remove.");
    }
  } catch (err) {
    console.error(err);
    alert("Error connecting to server.");
  }
}

// Random pick
async function randomPick() {
  const token = localStorage.getItem("token");
  const category = document.querySelector("#categorySelect").value || "";
  try {
    const res = await fetch(`${API_IDEAS}/random?category=${category}`, {
      headers: {
        "Authorization": `Bearer ${token}`,
        "accept": "application/json",
      },
    });

    if (res.status === 404) {
      alert("No ideas in this category.");
      return;
    }

    const idea = await res.json();
    alert(`✨ Random Pick ✨\n\n${idea.title}\n${idea.note || ""}`);
  } catch (err) {
    console.error(err);
    alert("Error fetching random idea.");
  }
}

// Button setup
document.addEventListener("DOMContentLoaded", () => {
  const randomBtn = document.getElementById("randomBtn");
  if (randomBtn) randomBtn.addEventListener("click", randomPick);

  const addBtn = document.querySelector(".add-button");
  if (addBtn) {
    addBtn.addEventListener("click", () => {
      window.location.href = "add.html";
    });
  }

  // 🩵 Filter event — reloads list whenever category changes
  const categorySelect = document.querySelector("#categorySelect");
  if (categorySelect) {
    categorySelect.addEventListener("change", loadMyJar);
  }

  loadMyJar();
});

// Logout button
document.getElementById("logoutBtn").addEventListener("click", () => {
  localStorage.removeItem("token");
  alert("You have been logged out!");
  window.location.href = "login.html";
});