# CR-backend

This backend API is built with Python and containerized using Docker. It allows users to upload PDF files, processes them to extract text content, and returns the extracted data to the frontend. The backend is hosted on Render.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Setup Environment](#setup-environment)
  - [Run Locally](#run-locally)

## Features

- Accepts PDF uploads via a POST request.
- Extracts text content from the uploaded PDF.
- Handles Unicode mapping issues gracefully.
- Returns extracted text as JSON to the client.
- Built with FastApi for simplicity and ease of deployment.
- Containerized with Docker for portability.

## Tech Stack

- **Python**: Core language.
- **FastApi**: Web framework for handling requests and responses.
- **PyPDF2 and Tabula**: Library for extracting text from PDFs.
- **Docker**: For containerizing the application.
- **Render**: Hosting platform for deployment.

## Prerequisites

Ensure you have the following installed:

- **Python** (v3.8 or later)
- **pip** (Python package manager)
- **Docker** (for containerized deployment)
- **Git** (for cloning the repository)

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/D3V1L1805/CR-backend.git
cd CR-backend
```

### Setup Environment

```bash
pip install -r requirements.txt
```

### Run Locally

run the router file using python directly 
or
```bash
uvicorn router:app --host 0.0.0.0 --port 5000
