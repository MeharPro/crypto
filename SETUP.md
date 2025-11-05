# Project Setup Guide

This guide provides a complete walkthrough for setting up and running the Ultimate iOS Trading Bot. Follow these steps to get the backend server and the iOS application running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+** and **pip**: For running the backend server.
*   **Xcode 13+**: For building and running the iOS application.
*   An **Alpaca Paper Trading Account**: To get the necessary API keys. You can sign up at [alpaca.markets](https://alpaca.markets/).

---

## Part 1: Backend Server Setup

Follow these steps to configure and run the Python Flask server.

### 1. Navigate to the Server Directory
Open your terminal and change into the `server` directory:
```bash
cd server
```

### 2. Create and Activate a Python Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

**Create the environment:**
```bash
python3 -m venv venv
```

**Activate the environment:**
*   On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```
*   On Windows:
    ```bash
    .\\venv\\Scripts\\activate
    ```
You'll know it's active when you see `(venv)` at the beginning of your terminal prompt.

### 3. Install Dependencies
Install all the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
The server needs your Alpaca API keys to connect to your paper trading account.

**Create a `.env` file:**
Copy the example environment file to create your own configuration file:
```bash
cp .env.example .env
```

**Edit the `.env` file:**
Open the newly created `.env` file in a text editor and replace the placeholder text with your actual Alpaca **Paper Trading** API keys.

```dotenv
# Your .env file should look like this:
APCA_API_KEY_ID='PXXXXXXXXXXXXXXXXXXX'
APCA_API_SECRET_KEY='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
APCA_API_BASE_URL='https://paper-api.alpaca.markets'
```
**Important:** Do not commit your `.env` file to version control. The `.gitignore` file is already configured to prevent this.

### 5. Run the Server
With your virtual environment active and API keys configured, you can now run the Flask server:
```bash
python -m flask run --port 5001
```
You should see output indicating that the server is running, similar to this:
```
 * Serving Flask app 'app'
 * Running on http://1227.0.0.1:5001
Press CTRL+C to quit
```
**Leave this terminal window open.** The server must be running for the iOS app to work.

---
## Part 2: iOS App Setup

These steps will guide you through running the iOS application.

### 1. Open the Xcode Project
Navigate to the `ios-app/TradingBot` directory and open the `TradingBot.xcodeproj` file. You can do this by double-clicking the file in Finder or using the terminal:
```bash
open ios-app/TradingBot/TradingBot.xcodeproj
```

### 2. Select a Simulator and Run the App
In Xcode's top bar, select a target simulator (e.g., "iPhone 14 Pro"). Then, click the **Run** button (the play icon) or press **Cmd+R**.

Xcode will build the app and launch it in the selected iOS Simulator.

---
## Part 3: Verification

Once both the server and the app are running, you can verify that they are communicating correctly.

1.  In the iOS app, the **Status** should initially say "Not Running".
2.  Click the **"Start Trading Bot"** button. The status should change to "Running".
3.  Check the terminal window where your Flask server is running. You should see a log message confirming the bot has started:
    ```
    Trading bot started.
    ```
4.  Navigate to the **Live Dashboard** in the app. The portfolio value should load and display a dollar amount.
5.  Click the **"Stop Trading Bot"** button. The status in the app should change to "Stopped", and you should see a "Trading bot stopped" message in the server logs.

If you can complete these steps, your setup is successful! You are now ready to use and develop the Ultimate iOS Trading Bot.
