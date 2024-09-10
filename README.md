# Ethereum Deposit Tracker

## Steps

1. Install dependencies (ensure you have python3.10 and virtualenv installed)
```bash
virtualenv venv
venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file with the following content: (given in sample.env)
```bash
BEACON_DEPOSIT_CONTRACT=0x00000000219ab540356cBB839Cbe05303d7705Fa
ETHEREUM_RPC_URL=https://eth-mainnet.alchemyapi.io/v2/o_53dnJWwjzLZ1npyP1NS7nUS74PqvcT
TELEGRAM_BOT_TOKEN=<>
TELEGRAM_CHAT_ID=<>
```

3. Run the script
```bash
python main.py
```

4. Check the DB
```bash
python read_db.py
```

5. Run using Docker
```bash
docker build -t my-python-app .
docker run my-python-app
```