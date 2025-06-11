💹 Gemini RSI Trading Bot
A Python-based automated trading bot that uses the Relative Strength Index (RSI) to make buy and sell decisions for Bitcoin via the Gemini API. Built with an object-oriented design for clarity, modularity, and ease of maintenance.

📁 Project Structure
gemini-rsi-bot/
├── broker.py   # Handles Gemini API integration and trade execution
├── main.py     # Gathers market data, calculates RSI, and makes trading decisions
├── README.md   # Project documentation
⚙️ Features

📈 RSI-Based Strategy: Uses the RSI indicator to identify overbought and oversold conditions.

🔁 Automated Trading: Executes buy/sell orders through Gemini's secure API.

🧱 Object-Oriented Design: Clean separation of concerns between trading logic and API handling.

🔐 Secure API Handling: Keeps your API keys safe and uses best practices for authentication.

🧠 How It Works
main.py:

Fetches real-time Bitcoin price data.
Calculates the RSI using historical price data.
Makes a decision to buy, sell, or hold based on RSI thresholds.
broker.py:

Connects to the Gemini API.
Executes trades securely.
Handles API authentication and error management.
📊 RSI Strategy
Buy Signal: RSI < 30 (oversold)
Sell Signal: RSI > 70 (overbought)
Hold: RSI between 30 and 70
These thresholds can be customized in the code to suit your trading preferences.

🚀 Getting Started
1. Clone the Repository

2. Install Dependencies

3. Set Up Environment Variables
Create a .env file with your Gemini API credentials:


4. Run the Bot

🛡️ Disclaimer
This bot is for educational purposes only. Trading cryptocurrencies involves significant risk. Use at your own discretion and always test thoroughly before deploying with real funds.

📬 Contributions
Contributions, issues, and feature requests are welcome! Feel free to fork the repo and submit a pull request.

-----
1 year update, bot has been successful on gemini sandbox API through bear and bull market. will activate live account.

------
.40% taker fee 
.20% maker fee
