# 📰 RSS Tracker and Notification Bot (Firestore & Telegram)

This project is a comprehensive application designed to automatically scrape RSS-like data from various internet sources, save this data to a Firebase Firestore database, and instantly notify you of new content via a Telegram bot.

⚠️ **DEVELOPER NOTICE:** This application is intended for users with Python programming skills and technical knowledge. It is not an end-user product, but rather a framework requiring experience in scraper development, API integration, and automation.

---

## ✨ Key Features
- **Multi-Source Support:** Ability to scrape data from diverse sites (e.g., Kızılay, Ministry of Health, official announcement sites, etc.).
- **Reliable Data Storage:** All scraped data is saved to the scalable and secure Firebase Firestore database.
- **Instant Notifications:** Automated and fast alerts via a Telegram Bot when new content is discovered.
- **Modular Architecture:** Utilizes a common FeedScraper class structure for easy integration of new scrapers.
- **Easy Integration:** Simple process for quickly adding new RSS or custom web scrapers.
- **Simple Configuration:** All settings are managed easily via the `.env` file.

---

## ⚙️ Setup and Installation
Follow these steps to quickly get the project running in your local environment.

### 1. Clone the Repository
```bash
git clone https://github.com/Muratoksuz01/Rss-Tracker.git
cd Rss-Tracker
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv

# For Linux/Mac
source .venv/bin/activate

# For Windows
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure the `.env` File
Create a `.env` file in the project root directory and fill in the following variables:

```env
FIREBASE_CREDENTIALS=<path>/firebase_api.json
TELEGRAM_BOT_TOKEN=<telegram-bot-token>
TELEGRAM_CHAT_ID=<target-chat-id>
```

---

## 🛠️ Service Configuration

### 🔥 Firebase Firestore Setup
1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2. Enable the Firestore Database choosing **"Production Mode."**
3. Navigate to **Settings → Project Settings → Service Accounts.**
4. Select **"Generate new private key"** and download the resulting JSON file.
5. Update the `FIREBASE_CREDENTIALS` variable in your `.env` file with the absolute path to this file (e.g., `config/firebase_api.json`).

### 🤖 Telegram Bot Setup
1. Start a chat with [@BotFather](https://t.me/BotFather) on Telegram and use the `/newbot` command to create a new bot. Get the **TOKEN**.
2. Add the bot to the target group/channel/chat and make it an administrator.

⭐ **Finding the chat_id:**
To easily find the chat ID, open the following URL in your browser, replacing `<TELEGRAM_BOT_TOKEN>` with your actual token:

```
https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates
```

In the resulting JSON output, find the `"id"` field within the `"chat"` object and add it to the `TELEGRAM_CHAT_ID` in your `.env` file.

---

## ➕ Adding New RSS Sources and Development
The power of this project lies in your ability to write custom scrapers using your Python knowledge (or with the help of AI/LLM tools).

💡 **Core Development Rule:**  
When adding a new source, you must override the `scrape()` method defined in `core/FeedScraper.py`.  
This method is defined as an abstract method in Python, and all your custom scraping logic must be placed here.  
Refer to the existing sources in the `scrapers/` folder for examples.

### 🔎 How to Find and Test CSS Selectors
To precisely target titles, links, or dates on a webpage, you must use **CSS Selectors**.

1. **Open the Target Page:** Open the web page you wish to scrape in a modern browser.  
2. **Inspect the Element:** Right-click on the element you want to extract and select **"Inspect"** to open the Developer Tools.  
3. **Copy the Selector:** Right-click on the selected HTML element in the Developer Tools. Select **Copy → Copy Selector.**

⭐ **Testing the Selector in the Browser Console:**
To ensure your copied selector correctly targets the desired elements, switch to the Console tab and execute the following JavaScript command:

```javascript
document.querySelectorAll("PASTE-SELECTOR-HERE");
```

If the command returns a list of the expected elements, your selector is ready to be used in your scraper class.

---

## 🚀 Running and Automation
- The main execution logic resides in the `main.py` file.  
- To have the project periodically check for new content, place the calls to all your added RSS classes inside a **while loop** (e.g., to run every 30 minutes) to start the automation.  
- To test a newly written class once, call the functions sequentially outside the loop: first `scrape()` → then `save_feed()` → and finally `notify()` to verify the data flow.
