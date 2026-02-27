# smart_shiksha_app

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## Configuration

This project uses `flutter_dotenv` to manage environment variables.

1.  Copy `.env.example` to `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Update the `API_BASE_URL` in `.env` to point to your backend server.
    *   For local development on Android emulator: `http://10.0.2.2:8000`
    *   For local development on iOS simulator: `http://localhost:8000`
    *   For production: Use a secure `https://` URL.

**Security Note:** In release mode, the app requires the `API_BASE_URL` to start with `https://`.
