const API_BASE = "http://127.0.0.1:8000/api"; // change if deployed later


// Save token in browser
export function saveToken(token) {
  localStorage.setItem("token", token);
}

// Retrieve token
export function getToken() {
  return localStorage.getItem("token");
}

// Remove token (for logout)
export function clearToken() {
  localStorage.removeItem("token");
}

// Add auth header automatically
function authHeaders() {
  const token = getToken();
  return token ? { "Authorization": `Bearer ${token}` } : {};
}

// Register new user
export async function registerUser(username, password) {
  const res = await fetch(`${API_BASE}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) throw new Error((await res.json()).detail || "Registration failed");
  return await res.json();
}

// Login existing user
export async function loginUser(username, password) {
  const res = await fetch(`${API_BASE}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) throw new Error("Invalid username or password");

  const data = await res.json();
  saveToken(data.access_token);
  return data;
}



// Create new idea
export async function createIdea(ideaData) {
  const res = await fetch(`${API_BASE}/ideas/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(ideaData),
  });

  if (!res.ok) throw new Error((await res.json()).detail || "Failed to create idea");
  return await res.json();
}

// Get public ideas
export async function getPublicIdeas() {
  const res = await fetch(`${API_BASE}/ideas/public`);
  return await res.json();
}

// Get user's jar (own + favorites)
export async function getMyJar() {
  const res = await fetch(`${API_BASE}/ideas/jar`, {
    headers: authHeaders(),
  });

  if (res.status === 401) throw new Error("Unauthorized. Please log in again.");
  return await res.json();
}

// Heart an idea
export async function heartIdea(id) {
  const res = await fetch(`${API_BASE}/ideas/heart/${id}`, {
    method: "POST",
    headers: authHeaders(),
  });
  return await res.json();
}

// Unheart an idea
export async function unheartIdea(id) {
  const res = await fetch(`${API_BASE}/ideas/heart/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return await res.json();
}