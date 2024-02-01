# Telegram Bot for Suggesting News

This is a Telegram bot that allows users to suggest news articles to a group chat. The bot stores the user's Telegram ID in a SQLite database and then forwards the suggested news articles to the group chat.

## Installation

1. Install the required dependencies:

```bash
pip install aiogram aiosqlite
```

2. Replace the following values with your own:

* `API_TOKEN`: Your Telegram bot's API token
* `GROUP_CHAT_ID`: The ID of the group chat where you want to forward news articles
* `FILE_OF_DB`: The path to the SQLite database file

## Usage

1. Start the bot:

```bash
python main.py
```

2. To suggest a news article, send a message to the bot 


3. Also you can send a message, replying to the suggester 
```
/sendmessage <PersonID> <Message>
```

Where `PersonID` is the ID of the person you want to send the message to, and `Message` is the replying message you want to send.

For example, to reply to a person with ID 123, you would send the following message:

```
/sendmessage 123 This is a great news article!
```

