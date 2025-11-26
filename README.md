# # Date Jar

A full-stack date planning web application built with FastAPI, PostgreSQL, and a vanilla JS + HTML/CSS frontend.
The app allows users to register, log in, create date ideas, set locations on a map, filter categories, save favorites (“Jar”), and explore public ideas on an interactive map.

The project includes end-to-end DevOps practices including automated tests, CI/CD via GitHub Actions, a production-ready Docker image, and deployment on Azure Web App.
Prometheus metrics and a health check endpoint are also enabled.

⸻

# Live Deployment

Azure Web App URL:
👉 https://date-jar.azurewebsites.net

⸻

Features

# User System
	•	Registration & login (JWT authentication)
	•	Token-based protected routes
	•	User-specific private ideas
	•	Favorites (heart/unheart)

# Idea System
	•	Create, edit, delete ideas
	•	Private/public visibility
	•	Multi-category tagging (max 3)
	•	Optional map location (Leaflet + OpenStreetMap)
	•	Random idea picker
	•	Personal “Jar” (own ideas + saved favorites)

# Interactive Map
	•	Public ideas shown as markers
	•	Popup preview & one-click saving
	•	Live user jar updates

# Engineering & DevOps
	•	FastAPI backend with SQLAlchemy ORM
	•	PostgreSQL (Azure Flexible Server)
	•	Docker container (production build)
	•	CI/CD pipeline with GitHub Actions
	•	Automated tests running on SQLite (TESTING mode)
	•	/api/health endpoint
	•	/metrics Prometheus metrics via prometheus-fastapi-instrumentator