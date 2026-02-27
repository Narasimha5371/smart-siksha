# Smart Shiksha Desktop App - Setup Instructions

Follow these steps to set up and run the Smart Shiksha Desktop Application entirely on a Windows environment. The application uses a Python FastAPI backend and a Flutter Windows frontend.

## Prerequisites

Before starting, ensure you have the following installed on your machine:

1. **Python 3.10+**: For the backend service.
2. **Flutter SDK**: Installed and configured for Windows development.
   - Run `flutter doctor` to verify you have the *Windows Desktop* toolchain installed.
3. **Visual Studio 2022**: Required by Flutter to build Windows desktop applications (ensure "Desktop development with C++" workload is selected during installation).
4. **Git**: For version control (optional but recommended).

---

## 1. Backend Setup (FastAPI)

The backend orchestrates the AI Tutor (using Groq LLaMA models) and mock test generation.

### Step 1.1: Navigate to Backend Directory
Open your terminal (PowerShell/Command Prompt) and navigate to the backend folder:
```bash
cd "c:\Users\naras\Desktop\Desktop(1)\smart siksha\backend"
```

### Step 1.2: Create and Activate a Virtual Environment
It's best practice to use a virtual environment to avoid dependency conflicts.
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 1.3: Install Dependencies
Install the required Python packages (FastAPI, Uvicorn, Requests, Groq, etc.):
```bash
pip install -r requirements.txt
```

### Step 1.4: Configure Environment Variables
1. Open the `.env` file located in the `backend` folder.
2. Ensure you have your `GROQ_API_KEY` set up.
3. (Optional) Make sure `USE_OLLAMA=false` to use the incredibly fast Groq API, or `USE_OLLAMA=true` if you prefer offline inferencing.

### Step 1.5: Start the Backend Server
Start the local FastAPI server:
```bash
python main.py
```
*The server will start running at `http://localhost:8000` or `http://127.0.0.1:8000`.* Keep this terminal window open.

---

## 2. Frontend Setup (Flutter Windows App)

The frontend is a Flutter-based UI built specifically to run natively on Windows.

### Step 2.1: Navigate to the Flutter App Directory
Open a **new** terminal window and navigate to the frontend folder:
```bash
cd "c:\Users\naras\Desktop\Desktop(1)\smart siksha\smart_shiksha_app"
```

### Step 2.2: Fetch Dependencies
Download all the required Flutter and Dart packages:
```bash
flutter pub get
```

### Step 2.3: Verify API Connections
The app connects to the backend through `lib/services/api_service.dart`. 
For Windows Desktop execution, the endpoint is set to use the explicit loopback address `http://127.0.0.1:8000` rather than `localhost` to prevent IPv6 DNS resolution lag. If you deploy the backend remotely, update `baseUrl` in this file.

### Step 2.4: Run the Application
Finally, compile and run the Windows desktop application:
```bash
flutter run -d windows
```
*The engine will build the C++ wrapper and launch the native Smart Shiksha learning dashboard.*
