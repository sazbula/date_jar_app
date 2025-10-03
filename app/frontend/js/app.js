// --- Tab switching ---
const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const message = document.getElementById("message");

loginTab.addEventListener("click", () => {
  loginTab.classList.add("active");
  registerTab.classList.remove("active");
  loginForm.classList.add("active");
  registerForm.classList.remove("active");
});

registerTab.addEventListener("click", () => {
  registerTab.classList.add("active");
  loginTab.classList.remove("active");
  registerForm.classList.add("active");
  loginForm.classList.remove("active");
});

// --- API base URL (change if needed) ---
const API_BASE = "http://127.0.0.1:8000"; // FastAPI local server

// --- Handle login ---
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access_token); // store JWT
      window.location.href = "map.html"; // redirect to map
    } else {
      message.textContent = data.detail || "Login failed.";
    }
  } catch (err) {
    message.textContent = "Error connecting to server.";
  }
});

// --- Handle register ---
registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("registerUsername").value;
  const password = document.getElementById("registerPassword").value;

  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();
    if (res.ok) {
      message.textContent = "Registration successful. You can now log in.";
    } else {
      message.textContent = data.detail || "Registration failed.";
    }
  } catch (err) {
    message.textContent = "Error connecting to server.";
  }
});