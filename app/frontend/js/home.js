const homeList = document.getElementById("homeIdeasList");

async function loadHomeIdeas() {
  homeList.innerHTML = "<p>Loading...</p>";
  try {
    // API: only at-home + public ideas
    const res = await fetch("http://127.0.0.1:8000/ideas?is_home=true&is_public=true");
    const ideas = await res.json();

    if (!ideas.length) {
      homeList.innerHTML = "<p>No at-home ideas yet.</p>";
      return;
    }

    homeList.innerHTML = "";
    ideas.forEach(idea => {
      const div = document.createElement("div");
      div.classList.add("idea-item");
      div.innerHTML = `
        <h2 class="idea-title">${idea.title}</h2>
        <p class="idea-note">${idea.note}</p>
        <button class="heart-btn">❤️ Heart</button>
      `;
      homeList.appendChild(div);
    });
  } catch (err) {
    homeList.innerHTML = "<p>Failed to load ideas.</p>";
  }
}

loadHomeIdeas();