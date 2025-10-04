import { loginUser, registerUser } from "./api.js";

// --- TAB SWITCHING LOGIC ---
const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");
const messageEl = document.getElementById("message");

loginTab.addEventListener("click", () => {
  loginTab.classList.add("active");
  registerTab.classList.remove("active");
  loginForm.classList.add("active");
  registerForm.classList.remove("active");
  messageEl.textContent = "";
});

registerTab.addEventListener("click", () => {
  registerTab.classList.add("active");
  loginTab.classList.remove("active");
  registerForm.classList.add("active");
  loginForm.classList.remove("active");
  messageEl.textContent = "";
});

// --- LOGIN FORM ---
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("loginUsername").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  try {
    const res = await loginUser(username, password);
    localStorage.setItem("token", res.access_token);
    messageEl.textContent = "Login successful!";
    messageEl.style.color = "#B185DB";

    // Redirect to home page after 1s
    setTimeout(() => {
      window.location.href = "home.html";
    }, 1000);
  } catch (err) {
    messageEl.textContent = "Invalid username or password.";
    messageEl.style.color = "red";
  }
});

// --- REGISTER FORM ---
registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("registerUsername").value.trim();
  const password = document.getElementById("registerPassword").value.trim();

  try {
    await registerUser(username, password);
    messageEl.textContent = "Registration successful! You can now log in.";
    messageEl.style.color = "#B185DB";

    // Switch to login tab automatically
    registerTab.classList.remove("active");
    loginTab.classList.add("active");
    registerForm.classList.remove("active");
    loginForm.classList.add("active");
  } catch (err) {
    messageEl.textContent = "Username already taken or error occurred.";
    messageEl.style.color = "red";
  }
});