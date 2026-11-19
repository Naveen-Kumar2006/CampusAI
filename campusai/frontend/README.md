# CampusAI — Frontend Portal

The client-side web application for CampusAI, built with React 19, TypeScript, Vite, and Tailwind CSS v4.

## Features

- **College Portal UI**: Responsive interface showcasing departments, announcements, upcoming events, and academics.
- **RAG Chatbot Assistant**: Embedded conversational interface interacting with the FastAPI backend (`/api/chat`).
- **Styling**: Modern, responsive design powered by Tailwind CSS v4.
- **Routing**: Client-side navigation handled by React Router v7.

## Tech Stack

- **React 19** + **TypeScript**
- **Vite 8**
- **Tailwind CSS v4** + **PostCSS**
- **Lucide React** (icons)
- **React Router DOM v7**

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

The application will start at `http://localhost:5173`. Ensure the FastAPI backend is running at `http://localhost:8000`.

### 3. Build for Production

```bash
npm run build
```

This compiles TypeScript (`tsc -b`) and bundles production assets into the `dist/` directory using Vite.

### 4. Preview Production Build

```bash
npm run preview
```
