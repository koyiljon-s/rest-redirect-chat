# Rest Redirect Chat API

A FastAPI-based chat application with user authentication, posts, and comments.

## Prerequisites

- Python 3.8+
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/koyiljon-s/rest-redirect-chat.git
   cd rest-redirect-chat
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```


## Running the Application

### Using Python

1. Run the FastAPI server:
   ```bash
   python src/main.py
   ```

2. The API will be available at `http://localhost:8081`

3. API documentation: `http://localhost:8081/docs`

### Using Docker

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:8081`
`