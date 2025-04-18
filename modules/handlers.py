from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from api_helpers import fetch_deposit_and_debt_from_api, fetch_customer_properties, fetch_debt_for_code, fetch_property_details, generate_financial_status_message, fetch_auth_token, format_number
from database_operations import check_user_exists, save_user, update_user_details, validate_and_fetch_mobile_number
from menu_helpers import Change_Assosiate_mobile, get_main_menu, display_blady_button 
import logging
import time

from translations import TRANSLATIONS  # Import the translations

from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegram.error import TimedOut  # Import the TimedOut exception
import httpx  # Import httpx if you're using it in your code

logger = logging.getLogger(__name__)

user_data = {}


import asyncio


logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    telegram_id = update.message.from_user.id
    first_name = update.message.from_user.first_name

    try:
        logger.info(f"Received /start command from telegram_id={telegram_id}")

        # Initialize user data with validation state
        user_data[telegram_id] = {"state": "step0_validate_phone"}

        # Create keyboard with Share Phone Number button
        keyboard = [
            [KeyboardButton(TRANSLATIONS["share_phone"], request_contact=True)]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

        # Send welcome message and prompt for phone number
        welcome_message = TRANSLATIONS["welcome_message"].format(name=first_name)
        await update.message.reply_text(welcome_message)
        await update.message.reply_text(TRANSLATIONS["ask_mobile_number"], reply_markup=reply_markup)

        logger.info(f"Initialized user data for telegram_id={telegram_id}")
        logger.info(f"Completed /start command for telegram_id={telegram_id} in {time.time() - start_time:.2f} seconds")

    except Exception as e:
        logger.error(f"Error in start function for telegram_id={telegram_id}: {str(e)}")
        await update.message.reply_text(TRANSLATIONS["error_occurred"])
        raise




import time
from telegram import ReplyKeyboardMarkup, KeyboardButton

async def copy_of_ShowMyObject_based_on_mobile_number(mobile_number_param, update, context):
    """
    Process the mobile number provided by the user and show their objects using KeyboardButton.
    """
    try:
        start_time = time.time()
        logger.info(f"Starting copy_of_ShowMyObject_based_on_mobile_number for {mobile_number_param}")

        # Normalize mobile number
        if mobile_number_param.startswith("+"):
            mobile_number_param = mobile_number_param[1:]  # Remove '+'
        elif mobile_number_param.startswith("0"):
            mobile_number_param = "374" + mobile_number_param[1:]  # Replace '0' with '374'

        # Fetch properties
        validation_response = fetch_customer_properties(mobile_number_param)
        logger.info(f"Fetched properties for {mobile_number_param}: {validation_response}")

        if validation_response and "customerProperties" in validation_response:
            properties = validation_response["customerProperties"]

            # Generate buttons and status messages for each object
            keyboard = []
            status_messages = []
            for prop in properties:
                code = prop["code"]
                obj_type = prop["type"]
                apartment = prop["apartment"]
                flat_number = prop["number"]

                # Fetch detailed property info for deposit and debt
                details = fetch_property_details(code)
                logger.info(f"Fetched details for {code}: {details}")
                if details:
                    deposit = details.get("deposit", 0)
                    debt = details.get("debt", 0)

                    # Generate financial status message
                    status_message = generate_financial_status_message(code, deposit, debt, apartment, obj_type, flat_number)
                    status_messages.append(status_message)

                    # Log the status message for debugging
                    logger.info(f"Generated status message for {code}: {status_message}")

                    # Add button for object
                    button_text = f"{code} ({obj_type})"
                    if not keyboard or len(keyboard[-1]) >= 2:  # Start a new row if the current row has 2 buttons
                        keyboard.append([])  # Add a new row
                    keyboard[-1].append(KeyboardButton(button_text))  # Add the button to the last row

            # Add Back and Refresh buttons
            keyboard.append([KeyboardButton(TRANSLATIONS["Back1"]), KeyboardButton(TRANSLATIONS["Refresh"])])


            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

            # Send status messages to user
            if status_messages:
                await update.message.reply_text(
                TRANSLATIONS["found_objects"].format(mobile_number_param=mobile_number_param),
                reply_markup=reply_markup
            )

                await update.message.reply_text("\n".join(status_messages))

                # await update.message.reply_text("Ընտրեք գույքը՝ վճարումների պատմությունը դիտելու համար։")

                await update.message.reply_text(
                TRANSLATIONS["select_object_to_see_history"],
                reply_markup=reply_markup
            )


            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            logger.info(f"Sending keyboard with objects: {keyboard}")
            


            # Update state and store previous state
            telegram_id = update.message.from_user.id
            user_data[telegram_id]["prev_state"] = user_data[telegram_id].get("state", "step1_mobile_register_succesfully")
            user_data[telegram_id]["state"] = "step2_mobile_register_succesfully_show_my_objects"

            logger.info(f"State: {user_data[telegram_id]['state']} | Prev State: {user_data[telegram_id]['prev_state']}")
            logger.info(f"Completed copy_of_ShowMyObject_based_on_mobile_number in {time.time() - start_time:.2f} seconds")

        else:
            logger.warning(f"No objects found for {mobile_number_param}")
            # No objects found, prompt user to change mobile number
            keyboard = [[KeyboardButton(TRANSLATIONS["change_mobile"])]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                TRANSLATIONS["ask_mobile_number"],
                reply_markup=reply_markup
            )

    except Exception as e:
        telegram_id = update.message.from_user.id
        logger.error(f"Unhandled exception in copy_of_ShowMyObject_based_on_mobile_number for telegram_id={telegram_id}: {e}")

        # Restart the session gracefully
        await update.message.reply_text(
            "An error occurred or your session is lost. Restarting your session..."
        )
        await start(update, context)  # Restart the bot session




async def show_payment_history(code, update, context):
    """
    Fetch and display the payment history for the selected object code.
    """
    try:
        logger.info(f"Fetching payment history for object code: {code}")

        # Fetch detailed property info
        details = fetch_property_details(code)
        logger.info(f"Fetched property details for {code}: {details}")

        if details and isinstance(details, dict):
            # Generate payment history
            transactions = details.get("transactionsPayInfo", [])
            if transactions:
                history = "\n".join([
                    f"{trans['payedDate']}: {format_number(trans['payedAmount'])}" for trans in transactions
                ])
                message = TRANSLATIONS["payment_history"].format(code=code, history=history)
            else:
                message = TRANSLATIONS["no_transactions"].format(code=code)

            # Send payment history to the user
            await update.message.reply_text(message)

            # Update user state to payment history
            telegram_id = update.message.from_user.id
            user_data[telegram_id]["prev_state"] = "step2_mobile_register_succesfully_show_my_objects"
            user_data[telegram_id]["state"] = "step4_mobile_register_succesfully_show_my_objects_show_payment_history"

            logger.info(f"Printed from show_payment_history - Current state: {user_data[telegram_id]['state']}, Prev state: {user_data[telegram_id]['prev_state']}")
        else:
            logger.error(f"Failed to fetch details for code: {code}")
            await update.message.reply_text(TRANSLATIONS["error_fetching_details"])

    except Exception as e:
        telegram_id = update.message.from_user.id
        logger.error(f"Unhandled exception in show_payment_history for telegram_id={telegram_id}: {e}")

        # Restart the session gracefully
        await update.message.reply_text(
            "An error occurred or your session is lost. Restarting your session..."
        )
        await start(update, context)  # Restart the bot session

# async def show_payment_history(code, update):
#     """
#     Fetch and display the payment history for the selected object code.
#     """
#     logger.info(f"Fetching payment history for object code: {code}")

#     # Fetch detailed property info
#     details = fetch_property_details(code)
#     logger.info(f"Fetched property details for {code}: {details}")

#     if details and isinstance(details, dict):

#         # Generate payment history
#         transactions = details.get("transactionsPayInfo", [])
#         if transactions:
#             history = "\n".join([
#                 f"{trans['payedDate']}: {format_number(trans['payedAmount'])}" for trans in transactions
                
#             ])

#             # history = "\n".join([
#             #     f"{trans['payedDate']}: {format_number(float(trans['payedAmount']))}" for trans in transactions
#             # ])

#             message = TRANSLATIONS["payment_history"].format(code=code, history=history)

#         else:
            
#             message = TRANSLATIONS["no_transactions"].format(code=code)


#         # Send payment history to the user
#         await update.message.reply_text(message)

#         # Update user state to payment history
#         telegram_id = update.message.from_user.id
#         user_data[telegram_id]["prev_state"] = "step2_mobile_register_succesfully_show_my_objects"
#         user_data[telegram_id]["state"] = "step4_mobile_register_succesfully_show_my_objects_show_payment_history"

#         state1 = user_data[telegram_id].get("state")
#         prev_state1 = user_data[telegram_id].get("prev_state")
#         logger.info(f"printed from show payment history Current state: {state1}, Current prev_state: {prev_state1}")
#     else:
#         logger.error(f"Failed to fetch details for code: {code}")
#         await update.message.reply_text(TRANSLATIONS["error_fetching_details"])


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    telegram_id = update.message.from_user.id
    user_input = update.message.text.strip()

    try:
        logger.info(f"Received text message from telegram_id={telegram_id}: {user_input}")

        # Check if user session exists
        if telegram_id not in user_data or "state" not in user_data[telegram_id]:
            logger.warning(f"Session lost for telegram_id={telegram_id}. Restarting session...")
            await update.message.reply_text(TRANSLATIONS["session_lost"])
            await start(update, context)  # Restart session
            return

        # Retrieve user state
        state = user_data[telegram_id].get("state")
        logger.info(f"Current state for telegram_id={telegram_id}: {state}")

        # Handle other states and commands, change_mobile is not used so we don't need to handle it
        if user_input == TRANSLATIONS["change_mobile"]:
            logger.info(f"User selected 'change_mobile' for telegram_id={telegram_id}")
            # Create keyboard with Share Phone Number button
            keyboard = [
                [KeyboardButton(TRANSLATIONS["share_phone"], request_contact=True)]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(TRANSLATIONS["ask_mobile_number"], reply_markup=reply_markup)
            user_data[telegram_id]["state"] = "step0_validate_phone"
            return

        elif user_input == "contact_with_us":
            logger.info(f"User selected 'contact_with_us' for telegram_id={telegram_id}")
            await update.message.reply_text("Share with us your problem")
            user_data[telegram_id]["state"] = "contact_with_us"
            logger.info("Save this info in DB later.")
            await display_blady_button(update)
            return

        # elif user_input == TRANSLATIONS["View_Report"]:
        #     # logger.info(f"View_Report ={telegram_id}")
        #     logger.info(f"Checking View_Report match: user_input='{user_input}' vs TRANSLATIONS['View_Report']='{TRANSLATIONS['View_Report']}'")

        #     GOOGLE_DOC_LINK = "https://docs.google.com/document/d/your_google_doc_id/view"
        #     await update.message.reply_text(f"Դուք կարող եք դիտել հաշվետվությունը այստեղ:: {GOOGLE_DOC_LINK}")
        #     return
        elif user_input.strip() == TRANSLATIONS["View_Report"]:
            logger.info(f"Matching View_Report: user_input='{user_input}' vs TRANSLATIONS['View_Report']='{TRANSLATIONS['View_Report']}'")
            
            GOOGLE_DOC_LINK = "https://drive.google.com/drive/folders/1_9mM8bYcJY0vNJOGYuXm43EBMFds-N4B"
            await update.message.reply_text(f"Դուք կարող եք դիտել հաշվետվությունն այստեղ՝ {GOOGLE_DOC_LINK}")
            return


        elif user_input == TRANSLATIONS["Refresh"]:
            logger.info(f"User selected 'Refresh' for telegram_id={telegram_id}")
            user_initialize = await initialize(telegram_id)

            if user_initialize:
                logger.info("Reinitialization successful. Displaying refreshed menu.")
                if user_initialize.get("mobile_number"):
                    mobile_number = user_initialize["mobile_number"]
                    logger.info(f"Handling 'show_my_object' for mobile number: {mobile_number}")
                    user_data[telegram_id]["prev_state"] = state or "step1_mobile_register_succesfully"
                    await copy_of_ShowMyObject_based_on_mobile_number(mobile_number, update, context)
                    return
            else:
                logger.warning("Reinitialization failed. No user found.")
                await update.message.reply_text("Your session has expired. Please restart the bot by pressing /start.")
                return

        elif user_input == TRANSLATIONS["yes_show_objects"]:
            logger.info(f"User selected 'yes_show_objects' for telegram_id={telegram_id}")
            user = check_user_exists(telegram_id)
            if user and user.get("mobile_number"):
                mobile_number = user["mobile_number"]
                logger.info(f"Handling 'show_my_object' for mobile number: {mobile_number}")
                user_data[telegram_id]["prev_state"] = state or "step1_mobile_register_succesfully"
                await copy_of_ShowMyObject_based_on_mobile_number(mobile_number, update, context)
            else:
                logger.warning(f"No mobile number found for user {telegram_id}")
                await update.message.reply_text(TRANSLATIONS["no_mobile_number_linked"])

        elif user_input.startswith(("A-", "P-", "C-")):
            logger.info(f"User selected object: {user_input}")
            code = user_input.split()[0]
            await show_payment_history(code, update, context)
            await display_blady_button(update)
            logger.info(f"Processed object selection in {time.time() - start_time:.2f} seconds")
            return

        elif user_input == TRANSLATIONS["Back1"]:
            logger.info(f"User selected 'Back1'. Restarting session for telegram_id={telegram_id}")
            await start_silently(update, context)
            return

        elif user_input == TRANSLATIONS["Blady"]:
            logger.info(f"User selected 'Blady'. Returning to previous object list.")
            mobile_number = get_associated_with_this_telegram_id_mobile_number(telegram_id)
            if mobile_number:
                await copy_of_ShowMyObject_based_on_mobile_number(mobile_number, update, context)
            else:
                logger.warning("Mobile number not found in database. Restarting session.")
                await start(update, context)
            return

        elif user_input == "Back12222":
            prev_state = user_data[telegram_id].get("prev_state")
            if not prev_state:
                logger.warning(f"No previous state found for telegram_id={telegram_id}. Inferring fallback state.")
                prev_state = {
                    "step4_mobile_register_succesfully_show_my_objects_show_payment_history": "step2_mobile_register_succesfully_show_my_objects",
                    "step2_mobile_register_succesfully_show_my_objects": "step1_mobile_register_succesfully"
                }.get(state, "step0_register_mobile")

            logger.info(f"User selected 'Back'. Previous state: {prev_state}")

            if prev_state == "step1_mobile_register_succesfully":
                logger.info("Returning to main menu.")
            elif prev_state == "step2_mobile_register_succesfully_show_my_objects":
                mobile_number = get_associated_with_this_telegram_id_mobile_number(telegram_id)
                if mobile_number:
                    await copy_of_ShowMyObject_based_on_mobile_number(mobile_number, update, context)
                else:
                    logger.warning("Mobile number missing. Restarting session.")
                    await start(update, context)
            elif prev_state == "step4_mobile_register_succesfully_show_my_objects_show_payment_history":
                await start(update, context)

            return

        elif state in ["step0_register_mobile", TRANSLATIONS["change_mobile"]]:
            logger.info(f"Handling mobile number input: State={state}, User Input={user_input}")
            validation_result = await validate_mobile_number(user_input)

            if validation_result == "not_valid_format":
                await update.message.reply_text(TRANSLATIONS["not_valid_format"])
                return
            elif validation_result == "valid_not_registered_in_API":
                await update.message.reply_text(TRANSLATIONS["valid_not_registered_in_API"])
                return

            save_user(telegram_id, user_input)
            logger.info(f"Mobile number {user_input} registered successfully for telegram_id={telegram_id}")
            user_data[telegram_id]["state"] = "step1_mobile_register_succesfully"
            await update.message.reply_text(TRANSLATIONS["mobile_number_saved"].format(new_mobile_number=user_input))
            await start(update, context)
            return

        # elif state == "step2_mobile_register_succesfully_show_my_objects":
        #     logger.info(f"User in step2_mobile_register_succesfully_show_my_objects selected: {user_input}")
        #     await update.message.reply_text("step1_mobile_register_succesfully Available options: choose buttons below")

        elif state == "step1_mobile_register_succesfully":
            await update.message.reply_text(TRANSLATIONS["unknown_command"])
            return  # Don't restart

        elif state == "step2_mobile_register_succesfully_show_my_objects":
            logger.info(f"User entered unexpected text in step2_mobile_register_succesfully_show_my_objects {user_input}")
            reply_markup = get_main_menu()
            await update.message.reply_text(TRANSLATIONS["unknown_command"], reply_markup=reply_markup)
            return  # Don't restart

        elif state == "step4_mobile_register_succesfully_show_my_objects_show_payment_history":
            logger.info(f"User entered unexpected text in step4_mobile_register_succesfully_show_my_objects_show_payment_history")
            await update.message.reply_text(TRANSLATIONS["unknown_command"])
            return  # Don't restart

                

        else:
            logger.warning(f"Unknown command or state for telegram_id={telegram_id}: {user_input}")
            await update.message.reply_text(TRANSLATIONS["unknown_command"])

    except Exception as e:
        logger.error(f"Unhandled exception in handle_text for telegram_id={telegram_id}: {e}")
        await update.message.reply_text(
            TRANSLATIONS["session_lost"]
        )
        await start(update, context)




def get_associated_with_this_telegram_id_mobile_number(telegram_id):
    """
    Fetch the mobile number associated with the given Telegram ID.
    """
    logger.info(f"Fetching mobile number for telegram_id={telegram_id}")
    user = check_user_exists(telegram_id)
    if user:
        mobile_number = user.get("mobile_number")
        logger.info(f"Mobile number found for telegram_id={telegram_id}: {mobile_number}")
        return mobile_number
    logger.warning(f"No mobile number found for telegram_id={telegram_id}")
    return None


# def get_step1_buttons():
#     """
#     Generate buttons for step1_mobile_register_succesfully.
#     """
#     logger.info("Generating buttons for step1_mobile_register_succesfully.")
#     keyboard = [
#         [KeyboardButton(TRANSLATIONS["yes_show_objects"])],
#         [KeyboardButton("change_mobile get_step1_buttons")],
#         [KeyboardButton("contact_with_us")]
#     ]
#     logger.info(f"Step1 buttons: {keyboard}")
#     return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def validate_mobile_number(mobile_number: str) -> str:
    """
    Validate the format and API registration of a mobile number.

    Args:
        mobile_number (str): The mobile number provided by the user.

    Returns:
        str: Validation result:
             - "valid_and_registered_in_API"
             - "not_valid_format"
             - "valid_not_registered_in_API"
    """
    logger.info(f"Validating mobile number: {mobile_number}")

    # Check format
    if not (mobile_number.startswith("+374") and len(mobile_number) == 12) and \
       not (mobile_number.startswith("0") and len(mobile_number) == 9) and \
       not (mobile_number.startswith("374") and len(mobile_number) == 11):
        logger.warning(f"Mobile number does not match required format: {mobile_number}")
        return "not_valid_format"

    # Check API validation
    logger.info(f"Mobile number format valid. Checking registration via API: {mobile_number}")
    response = await validate_and_fetch_mobile_number(mobile_number)  # Assume this function interacts with the API
    if response:
        logger.info(f"Mobile number {mobile_number} is registered in the API.")
        return "valid_and_registered_in_API"
    else:
        logger.info(f"Mobile number {mobile_number} is not registered in the API.")
        return "valid_not_registered_in_API"


async def display_properties(validation_response, update):
    """
    Display details of each property in the validation response.
    """
    logger.info(f"Starting display_properties with validation_response: {validation_response}")
    
    customer_properties = validation_response.get("customerProperties", [])
    logger.info(f"Extracted customer_properties: {customer_properties}")
    
    if not customer_properties:
        logger.warning("No properties found in validation_response")
        await update.message.reply_text("No properties found.")
        return

    try:

        for prop in customer_properties:
            logger.info(f"Processing property: {prop}")
            
            # Extract property details
            code = prop.get("code", "N/A")
            obj_type = prop.get("type", "N/A")
            apartment = prop.get("apartment", "N/A")
            number = prop.get("number", "N/A")
            # mobile_number_param = prop.get("phoneNumber", "N/A")

            logger.info(f"Extracted details - code: {code}, type: {obj_type}, apartment: {apartment}, number: {number}")

            message = (
                f"{TRANSLATIONS['property_details']}:\n"
                f"{TRANSLATIONS['property_type']} {obj_type}\n"
                f"{TRANSLATIONS['property_code']} {code}\n"
                f"{TRANSLATIONS['property_address']} {apartment}\n"
                f"{TRANSLATIONS['property_number']} {number}"
            )

            logger.info(f"Prepared message to send: {message}")

            # Send the message
            try:
                await update.message.reply_text(message)
                logger.info(f"Successfully sent message for property {code}")
            except Exception as e:
                logger.error(f"Error sending message for property {code}: {str(e)}")
                raise

    except Exception as e:
        logger.error(f"Error in display_properties: {str(e)}")
        raise

    logger.info("Completed display_properties successfully")


async def initialize(telegram_id):
    """
    Initialize user data and fetch user information from the database.

    Args:
        telegram_id (int): The Telegram ID of the user.

    Returns:
        dict: The user's data if found, or None if the user doesn't exist.
    """
    logger.info(f"Initializing data for telegram_id={telegram_id}")

    # If user_data doesn't exist, treat it as an expired session
    if telegram_id not in user_data:
        logger.warning(f"No session data found for telegram_id={telegram_id}. Treating as a new session.")

    # Check if the user exists in the database
    user = check_user_exists(telegram_id)
    logger.info(f"User data fetched from database: {user}")

    if user and user.get("mobile_number"):
        mobile_number = user["mobile_number"]
        logger.info(f"Fetching customer properties for mobile number: {mobile_number}")

        # Fetch customer properties
        validation_response = fetch_customer_properties(mobile_number)
        logger.info(f"Fetched properties: {validation_response}")

        # Reinitialize user_data for the user
        user_data[telegram_id] = {
            "state": "step1_mobile_register_succesfully",
            "prev_state": None,  # No previous state in a new session
            "mobile_number": mobile_number,
            "customer_properties": validation_response.get("customerProperties", []),
        }

        return user

    logger.warning(f"User with telegram_id={telegram_id} not found in database.")
    return None



async def start_silently(update: Update, context: ContextTypes.DEFAULT_TYPE):

    start_time = time.time()

    telegram_id = update.message.from_user.id

    if telegram_id not in user_data:
        user_data[telegram_id] = {"state": "step0_register_mobile"}  # Initialize user data
        logger.info(f"Initialized user data for telegram_id={telegram_id}")

    
    first_name = update.message.from_user.first_name  # Retrieve the user's first name
    logger.info(f"Received /start command from telegram_id={telegram_id} with name={first_name}")




    # Fetch and format the welcome message
    welcome_message = TRANSLATIONS["welcome_message"].format(name=first_name)

    user = check_user_exists(telegram_id)
    logger.info(f"User check returned: {user}")

    if user:
        logger.info("User found in database. Proceeding to main menu.")
        # await update.message.reply_text(welcome_message)
        mobile_number = user.get("mobile_number", "Not available")

        # Inform user if the server is down
        if not fetch_auth_token():
            await update.message.reply_text("There is a technical issue with the server. Please try again later.")
            return

        x = fetch_customer_properties(mobile_number)
        logger.info(f"Customer properties fetched: {x}")


        
        # message1 = f"{TRANSLATIONS['mobile_saved_in_db_found']} : {mobile_number}\n\n"
        # await update.message.reply_text(message1)

        await display_properties(x, update)

        # await update.message.reply_text(message)

        reply_markup = get_main_menu()
        await update.message.reply_text(TRANSLATIONS["ask_to_view_details"], reply_markup=reply_markup)

        user_data[telegram_id] = {"state": "step1_mobile_register_succesfully"}  # Set state after successful registration

    else:

        
        # Inform user if the server is down
        if not fetch_auth_token():
            await update.message.reply_text("There is a technical issue with the server. Please try again later.")
            return

        user_data[telegram_id] = {"state": "step0_register_mobile"}  # Set state for first-time login
        await update.message.reply_text(welcome_message)
        await update.message.reply_text(TRANSLATIONS["ask_mobile_number"])
    
    logger.info(f"Completed /start command in {time.time() - start_time:.2f} seconds")


async def handle_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    telegram_id = update.message.from_user.id
    
    try:
        logger.info(f"Starting phone number validation for telegram_id={telegram_id}")

        # Get the contact object from the message
        contact = update.message.contact
        if not contact:
            logger.error(f"No contact received from telegram_id={telegram_id}")
            await update.message.reply_text(TRANSLATIONS["error_occurred"])
            return

        # Extract phone number from contact
        phone_number_from_telegram = contact.phone_number
        logger.info(f"Received phone number from telegram_id={telegram_id}: {phone_number_from_telegram}")

        # Remove the + symbol if present
        if phone_number_from_telegram.startswith("+"):
            phone_number = phone_number_from_telegram[1:]
        else:
            phone_number = phone_number_from_telegram


        # Check if user exists in API
        # phone_number="37455102018"
        logger.info(f"Calling API to validate phone number: {phone_number}")
        validation_response = fetch_customer_properties(phone_number)
        logger.info(f"API response for phone number >>>>aaa>>. {phone_number}: {validation_response}")
        
        if validation_response and "customerProperties" in validation_response:
            # User exists in API, save to database and proceed
            logger.info(f"Phone number {phone_number} is valid and registered in API")
            save_user(telegram_id, phone_number)
            user_data[telegram_id]["state"] = "step1_phone_validated"
            
            # Show user's properties
            await display_properties(validation_response, update)
            reply_markup = get_main_menu()
            await update.message.reply_text(TRANSLATIONS["ask_to_view_details"], reply_markup=reply_markup)
        else:
            # User not found in API
            logger.warning(f"Phone number {phone_number} is not registered in API")
            await update.message.reply_text(TRANSLATIONS["valid_not_registered_in_API"])

        logger.info(f"Completed phone number validation for telegram_id={telegram_id} in {time.time() - start_time:.2f} seconds")

    except Exception as e:
        error_msg = f"Error in handle_phone_number for telegram_id={telegram_id}: {str(e)}"
        logger.error(error_msg)
        await update.message.reply_text(TRANSLATIONS["error_occurred"])
        raise

