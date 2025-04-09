# Telegram Bot Project

## Overview
This project is a Telegram bot built using Python and the `python-telegram-bot` library. It is designed to handle user interactions, manage reminders, and perform various operations through commands and messages. The bot integrates with a MySQL database to store and manage user information and communicates with an external API for customer validation and property information.

## Features
- **Start Command**: Initiates interaction with the bot using the `/start` command.
- **Text Handling**: Processes user text messages and responds accordingly.
- **Global Exception Handling**: Manages unexpected exceptions, including timeouts, to ensure a smooth user experience.
- **Database Operations**: 
  - Connects to a MySQL database to check if users exist, save user details, and update user information.
  - Validates and normalizes mobile numbers before saving them to the database.
- **API Interactions**: 
  - Fetches authentication tokens and customer properties from an external API.
  - Retrieves financial information such as deposits and debts associated with properties.
- **User State Management**: Maintains user states to track their progress and interactions with the bot.
- **Logging**: Configures logging for monitoring bot activity and errors.

## Handlers
The bot uses various handlers to manage user interactions:
- **`start(update, context)`**: Handles the `/start` command, initializes user data, and fetches customer properties.
- **`handle_text(update, context)`**: Processes user text input, manages state transitions, and responds to user commands.
- **`copy_of_ShowMyObject_based_on_mobile_number(mobile_number_param, update, context)`**: Displays properties associated with the user's mobile number.
- **`show_payment_history(code, update, context)`**: Fetches and displays the payment history for a selected property.
- **`validate_mobile_number(mobile_number)`**: Validates the format and API registration of a mobile number.

## API Operations
The bot interacts with an external API to manage customer data. Key functions include:
- **`fetch_auth_token()`**: Retrieves an access token for API authentication.
- **`fetch_customer_properties(mobile_number)`**: Validates a mobile number and fetches associated customer properties.
- **`fetch_deposit_and_debt_from_api(unique_code)`**: Retrieves deposit and debt information for a property using its unique code.
- **`fetch_property_details(code)`**: Fetches detailed property information, including payment history, debt, and deposit.
- **`generate_financial_status_message(...)`**: Creates a formatted message summarizing the financial status of a property.

## Installation
To set up the project, clone the repository and install the required dependencies.

```bash
# Clone the repository
git clone https://github.com/yourusername/yourproject.git

# Navigate to the project directory
cd yourproject

# Install dependencies
pip install -r requirements.txt
```

## Configuration
1. Create a `credentials.json` file in the project root with the following structure:
   ```json
   {
       "bot_token": "YOUR_BOT_TOKEN"
   }
   ```
2. Ensure you have a MySQL database set up and update the connection details in `database_operations.py` as needed.
3. Update the API credentials in the `fetch_auth_token()` function within `api_helpers.py`.

## Usage
Run the main application to start the bot.

```bash
python modules/main.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, please reach out to [Your Name](mailto:your.email@example.com).