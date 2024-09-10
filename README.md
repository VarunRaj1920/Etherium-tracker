# Ethereum Deposit Tracker 👾

<span>The Ethereum <img src="https://github.com/user-attachments/assets/8b5d0488-bdde-46f1-9d26-626124f7a7b4" height=20 width=20 />  Deposit Tracker is a robust, efficient, and dockerized **Python** application designed to monitor and record ETH deposits on the Beacon Deposit Contract. It provides real-time tracking and alerting of deposit data. </span>

## Features 🚀

1. **Real-time Deposit Tracking** 🕵️‍♂️: Monitors the Ethereum blockchain for deposits to the Beacon Deposit Contract.
2. **Telegram Notifications** 📱: Sends real-time alerts for new deposits via Telegram bot.
3. **Docker Support** 🐳: Containerized for easy deployment and scalability.
4. **Comprehensive Logging** 📊: Detailed logging for troubleshooting and auditing.

## Technologies Used 🛠️

- **Python 3.10** 🐍: Core programming language
- **Web3.py v5** 🌐: Ethereum interaction library
- **Telegram Bot API** 💬: Real-time notifications
- **Docker** 🐳: Containerization
- **dotenv** 🔐: Environment variable management

## Code Quality and Best Practices 💎

- **Environment Variable Management** 🔒: Securely manages configuration using `.env` files.
- **Error Handling** 🛡️: Comprehensive try/except blocks with detailed error logging.
- **Code Modularization** 🧩: Well-structured code with clear separation of concerns.
- **Type Hinting** 📝: Improves code readability and IDE support.

## Docker Support 🐳

- **Dockerfile** 📄: Optimized Dockerfile for building the application container.

## Steps to run 🏃‍♂️

1. Install dependencies (ensure you have python3.10 and virtualenv installed)
```bash
virtualenv venv
venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file with the following content: (given in sample.env)
(Assuming you have the api keys🙃)
```bash
BEACON_DEPOSIT_CONTRACT=0x00000000219ab540356cBB839Cbe05303d7705Fa
ETHEREUM_RPC_URL=https://eth-mainnet.alchemyapi.io/v2/<add alchemy api key>
TELEGRAM_BOT_TOKEN=<insert telegram bot token form fatherbot>
TELEGRAM_CHAT_ID=<insert chat id>
```

3. Run the script 🚀
```bash
python main.py
```

4. Check the DB 🔍
```bash
python read_db.py
```

5. Run using Docker 🐳
```bash
docker build -t my-python-app .
docker run my-python-app
```

Done!!! 🎉🎉🎉
