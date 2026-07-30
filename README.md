# AI Video Generator

Generate short AI videos from a text prompt using the Replicate AI Video Generation API.

---

## 1. Project Overview

This is a full-stack web application.

### Backend
- FastAPI
- SQLAlchemy (Async ORM)
- PostgreSQL

### Frontend
- React
- Vite
- Tailwind CSS
- Axios

### AI Provider
- Replicate API

The user enters a text prompt, the backend sends it to the Replicate API to generate a video, stores the generation history in PostgreSQL, and displays the generated video with a download option.

The application automatically keeps only the latest **5** generated videos by removing the oldest record whenever a new one is created.