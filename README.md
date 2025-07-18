# Discord Bot

A feature-rich Discord bot built with Python and discord.py that provides moderation, fun commands, and utility features for Discord servers.

## Features

### 🔧 Basic Commands
- `!hello` - Greet the user
- `!ping` - Check bot latency
- `!info` - Display bot information

### 🛡️ Moderation Commands
- `!kick @user [reason]` - Kick a member from the server
- `!ban @user [reason]` - Ban a member from the server
- `!clear [amount]` - Delete messages from the channel (max 100)

### 🎮 Fun Commands
- `!roll [sides]` - Roll a dice (default 6 sides, max 100)
- `!8ball [question]` - Magic 8-ball responses
- `!joke` - Get a random joke

### 📊 Utility Commands
- `!serverinfo` - Display server information
- `!userinfo [@user]` - Display user information
- `!avatar [@user]` - Show user's avatar
- `!help` - Show all available commands

### 🎉 Additional Features
- Welcome messages for new members
- Error handling with user-friendly messages
- Command cooldowns to prevent spam
- Rich embeds for better visual experience

## Prerequisites

- Python 3.8 or higher
- A Discord bot token (from Discord Developer Portal)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your bot token:
```
DISCORD_BOT_TOKEN=your_bot_token_here
```

4. Run the bot:
```bash
python secure_main.py
```

> **Note**: Use `secure_main.py` for the production-ready version with enhanced security features, or `main.py` for the basic version.

## Setup Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. In the "Bot" section, enable the following Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
6. Go to OAuth2 > URL Generator
7. Select "bot" in scopes and the following permissions:
   - Send Messages
   - Manage Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
   - Kick Members (if using moderation features)
   - Ban Members (if using moderation features)
8. Use the generated URL to invite your bot to your server

## Configuration

The bot uses environment variables for configuration. Make sure to create a `.env` file with:

```
DISCORD_BOT_TOKEN=your_discord_bot_token
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you need help or have questions:
- Create an issue in this repository
- Check the Discord.py documentation: https://discordpy.readthedocs.io/

## Changelog

### v1.0.0
- Initial release
- Basic bot commands
- Moderation features
- Fun commands
- Utility commands
- Welcome system
