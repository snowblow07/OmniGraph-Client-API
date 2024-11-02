# OmniGraph Client & API

**OmniGraph Client & API** is a comprehensive ecosystem designed for web and mobile clients to deliver graph-augmented insights through a powerful RESTful API and an interactive web interface. At its core, the project features an AI-powered "Super Trainer" agent that leverages LangChain and Google's Gemini models, with a Neo4j graph database backend for persistent, context-aware conversation history.

## 🚀 Overview

This project provides a seamless integration between advanced LLM capabilities and graph database technology. It is designed to be a "lean learning" system that evolves with user interactions, making it ideal for business training, customer support, and real-time knowledge delivery.

### Key Features

-   **🧠 AI-Powered Agent:** Built with LangChain and Google Gemini (Flash/Pro) for high-quality, context-aware responses.
-   **🕸️ Graph-Augmented Memory:** Uses **Neo4j** to store and retrieve chat histories, ensuring that every session is persistent and structurally organized.
-   **🌐 Dual-Access Ecosystem:**
    -   **Web Client:** A responsive, interactive chat widget that can be easily integrated into any web application.
    -   **RESTful API:** A robust backend API (`/agent`) that allows mobile and external clients to consume the agent's services.
-   **🔄 Dynamic Session Management:** Automatically handles multi-session tracking via unique identifiers and browser cookies.
-   **⚡ Real-Time Feedback:** Includes a polished UI with typing animations and smooth message transitions for an enhanced user experience.
-   **📱 Mobile Ready:** Designed with a vision for ARM architecture compatibility, enabling future deployment on iOS and Android devices.

## 🛠️ Tech Stack

-   **Backend:** Python, [Flask](https://flask.palletsprojects.com/), [Flask-CORS](https://flask-cors.readthedocs.io/)
-   **AI Framework:** [LangChain](https://www.langchain.com/), [Google Generative AI](https://ai.google.dev/) (Gemini)
-   **Database:** [Neo4j](https://neo4j.com/) (Graph Database)
-   **Frontend:** Vanilla HTML5, CSS3, JavaScript (ES6+)
-   **Environment:** [Python-Dotenv](https://saurabh-kumar.com/python-dotenv/) for secure configuration

## 📂 Project Structure

```text
.
├── agent.py            # Core AI logic, LangChain orchestration, and Neo4j integration
├── app.py              # Flask application and RESTful API endpoints
├── wsgi.py             # WSGI entry point for production deployment
├── requirements.txt    # Project dependencies
├── static/
│   ├── gemini01.css    # Modern UI styling for the chat widget
│   ├── images/         # UI assets and icons
│   └── util/
│       └── gemini01.js # Client-side chatbot logic and API communication
└── templates/
    └── agent.html      # Main web interface and landing page
```

## ⚙️ Installation & Setup

### Prerequisites

-   Python 3.8+
-   A Neo4j Database instance (e.g., [Neo4j AuraDB](https://neo4j.com/cloud/aura/))
-   A Google AI API Key (Gemini)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/manuel-rosero/omnigraph-client-api.git
    cd omnigraph-client-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your credentials:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    NEO4J_URI=your_neo4j_uri_here
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=your_neo4j_password_here
    ```

5.  **Run the application:**
    ```bash
    python app.py
    ```
    The app will be available at `http://localhost:5050`.

## 📡 API Usage

The system exposes a POST endpoint for external clients:

**Endpoint:** `/agent`
**Method:** `POST`
**Body:**
```json
{
  "message": "Hello, how can you help me today?",
  "config": "unique-session-id"
}
```

## 👤 Author

**Manuel Rosero Puente**
-   GitHub: [@snowblow07](https://github.com/snowblow07/OmniGraph-Client-API) 
-   LinkedIn: [Manuel Rosero Puente](https://www.linkedin.com/in/mroserop)

---