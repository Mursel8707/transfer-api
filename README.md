# Transfer API

This repository contains a simple FastAPI application for handling transfer bookings and sending notifications to Telegram.

## Setup

1. Copy `.env.example` to `.env` and fill in your credentials.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run the application with `uvicorn main:app --host 0.0.0.0 --port 10000`.

### Environment file

Create a `.env` file with the following content:

```env
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
```

The application uses `python-dotenv`'s `load_dotenv()` to read environment variables from `.env`. The Render deployment configuration (`render.yaml`) also loads variables from `.env`.

### Replacing a leaked Telegram token

If the Telegram bot token from earlier commits has been exposed, generate a new token using [BotFather](https://core.telegram.org/bots#botfather) and update the `.env` file.

To scrub the old token from git history, you can use `git filter-branch` or [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/). For example:

```bash
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch env' --prune-empty --tag-name-filter cat -- --all
```

After rewriting history, force-push the cleaned branch to replace the previous commits.

For more details see GitHub's guide on [removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
