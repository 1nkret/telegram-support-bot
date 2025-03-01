# Telegram Support Bot

The Telegram Support Bot is a Python-based solution designed to facilitate seamless communication between users and 
support staff within the Telegram platform. Leveraging the aiogram framework, this bot allows users to submit support 
requests, which are then efficiently managed and addressed by the support team.

## Features

- **User-Friendly Support Requests**: Users can effortlessly send messages to the bot, initiating support requests that 
are forwarded to a designated support group.
- **Real-Time Communication**: Support staff can respond directly to user inquiries through the support group, with 
messages relayed back to the user via the bot.
- **Multimedia Support**: The bot handles various message types, including text, photos, documents, and stickers, 
ensuring comprehensive support interactions.
- **Spam Protection**: Integrated mechanisms detect and filter out spam messages, maintaining the integrity of support 
communications.
- **User Management**: Support staff have the ability to ban or unban users, controlling who can interact with the bot.
- **FAQ Integration**: Users can access a customizable FAQ section, providing immediate answers to common questions.

## Installation

To deploy the Telegram Support Bot, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/1nkret/telegram-support-bot.git
   cd telegram-support-bot
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Bot**:
   - Rename the `.env.example` file to `.env`.
   - Edit `.env` to include your bot's token and the chat ID of the support group.

5. **Run the Bot**:
   ```bash
   python main.py
   ```

## Usage

- **Users**:
  - Start the bot by sending the `/start` command.
  - Submit support requests by sending messages directly to the bot.

- **Support Staff:**
  - Receive user messages in designated forum topics for each support request.
  - Each new ticket opens a dedicated forum thread where support staff can manage the request.
  - Use inline buttons within the thread to take, transfer, pause, or close tickets.
  - Communicate with users directly from the forum topic, with messages relayed to the bot.

## Contributing

Contributions to the Telegram Support Bot are welcome. Whether it's reporting bugs, suggesting features, or submitting 
pull requests, your input is valuable. Please ensure that any contributions align with the project's coding standards 
and include appropriate tests.

## License

This project is licensed under the MIT License. For more details, refer to the `LICENSE` file in the repository.

## Acknowledgements

This bot was developed using the aiogram framework and inspired by similar projects in the community. Special thanks to 
all contributors who have provided feedback and improvements.

---

For more information and updates, visit the [GitHub repository](https://github.com/1nkret/telegram-support-bot).

