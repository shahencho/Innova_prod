
import requests
import logging

logger = logging.getLogger(__name__)

TOKEN = None

def fetch_auth_token():
    global TOKEN
    try:
        url = "https://housing-api.technologist.ai/api/Authentication/accessToken"
        payload = {"email": "telegram@client.am", "password": "123456"}
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        TOKEN = data.get("accessToken")
        logger.info(f"Token fetched successfully: {TOKEN}")
        return TOKEN
    except requests.exceptions.HTTPError as e:
        if response.status_code == 502:
            logger.error("Server error: 502 Bad Gateway. Please try again later.")
        else:
            logger.error(f"HTTPError occurred: {e}")
        TOKEN = None
        return None
    except Exception as e:
        logger.error(f"Token fetch failed: {e}")
        TOKEN = None
        return None


def fetch_deposit_and_debt_from_api(unique_code):
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_auth_token()
        if not TOKEN:
            logger.error("Unable to fetch token. Aborting API call.")
            return None, None

    try:
        url = f"https://housing-api.technologist.ai/api/Customer/telegram/getPropInfo?code={unique_code}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(url)

                # Log the full API response
        logger.info(f"API Response for {unique_code}: {data}")   
        return data.get("deposit"), data.get("debt")
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None, None
    
def fetch_customer_properties(mobile_number):
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_auth_token()
        if not TOKEN:
            logger.error("Unable to fetch Bearer token. Aborting API call.")
            return None

    # mobile_number="37455024479" 
    
    # this is the mobile number of the customer just to test the api , we will remove it later
 

    try:
        # mobile_number="37455102018" 
        url = f"https://housing-api.technologist.ai/api/Customer/telegram/validation?phoneNumber={mobile_number}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        logger.info(f"Calling validation API with URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Validation API call failed: {e}")
        return None

def fetch_debt_for_code(code):
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_auth_token()
        if not TOKEN:
            logger.error("Unable to fetch Bearer token. Aborting API call.")
            return None

    try:
        url = f"https://housing-api.technologist.ai/api/Customer/telegram/getPropInfo?code={code}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        logger.info(f"Calling getPropInfo API with URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    
        return data.get("debt")
    except Exception as e:
        logger.error(f"getPropInfo API call failed for code {code}: {e}")
        return None



def fetch_property_details(code):
    """
    Fetches detailed property information including payment history, debt, and deposit.
    """
    global TOKEN
    if not TOKEN:
        TOKEN = fetch_auth_token()
        if not TOKEN:
            logger.error("Unable to fetch Bearer token. Aborting API call.")
            return None

    try:
        url = f"https://housing-api.technologist.ai/api/Customer/telegram/getPropInfo?code={code}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        logger.info(f"Calling getPropInfo API with URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        logger.info(f"API response for property details: {data}")
        return data
    except Exception as e:
        logger.error(f"API call failed for property details. Error: {e}")
        return None


    # Helper function to format numbers with commas
def format_number(value):
    return f"{value:,.2f}"



def generate_financial_status_message(code, deposit, debt, apartment, type_of_object, flat_number):
    """
    Generate a financial status message for a property.

    Args:
        code (str): The property code (e.g., "A-48-2").
        deposit (float): The deposit amount for the property.
        debt (float): The debt amount for the property.
        apartment (str): The apartment location of the property.
        type_of_object (str): The type of the object (e.g., "Բնակարան").
        flat_number (str): The flat number associated with the property.

    Returns:
        str: A formatted status message.
    """


    # Header information
    message = (
        f"-----------------------\n"
        f"Գույք համար: {code} ({type_of_object})\n"
        f"Շենք: {apartment}\n"
        f"N: {flat_number}\n"
        f"Կանխավճար: {format_number(deposit)} \n"
        f"Պարտք: {format_number(debt)} \n\n"
    )

    # Handle debt
    if debt < 0:
        message += (
            f"Դուք ունեք պարտք՝ {format_number(abs(debt))}։ Խնդրում ենք հնարավորինս շուտ կատարել վճարումը։\n"
        )
        # Add payment instructions for debt
        message += (
            "Վճարում կարող եք իրականացնել ինչպես բանկային փոխանցումով, այնպես էլ idram, Easy Wallet, "
            "Tel Cell, Fast Shift հավելվածներով և Tel Cell, EasyPay, FastShift տերմինալներով։\n"
            "Բանկային փոխանցման համար:\n"
            "Հաշվեհամար՝ 1660030213905000\n"
            "Բանկ՝ էվոկաբանկ\n"
            "Ստացող՝ «Վերածնունդ թաղամաս համատիրություն»\n"
            "Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի վճարման կոդը:\n"
        )
    elif debt > 0:
        message += (
            f"Դուք ունեք կանխավճար՝ {format_number(debt)}։ Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
        )

    # Include deposit if it exists
    if deposit > 0:
        message += (
            f"Դուք ունեք կանխավճար՝ {format_number(deposit)}։\n"
            "Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
        )

    # Zero balance case
    if debt == 0 and deposit == 0:
        message += "Ձեր հաշվեկշիռը նորմալ է։ Մնում է զրոյական հաշվեկշիռ։\n"

    return message

# def generate_financial_status_message(code, deposit, debt, apartment, type_of_object, flat_number):
#     """
#     Generate a financial status message for a property.

#     Args:
#         code (str): The property code (e.g., "A-48-2").
#         deposit (float): The deposit amount for the property.
#         debt (float): The debt amount for the property.
#         apartment (str): The apartment location of the property.
#         type_of_object (str): The type of the object (e.g., "Բնակարան").
#         flat_number (str): The flat number associated with the property.

#     Returns:
#         str: A formatted status message.
#     """
#     # Header information
#     message = (
#         f"Գույք համար: {code}\n"
#         f"{apartment}\n"
#         f"N: {flat_number} \n\n"
#     )

#     # Handle debt and deposit
#     if debt < 0:
#         message += (
#             f"Դուք ունեք կանխավճար՝ {abs(debt)}։ Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
#         )
#     elif debt > 0:
#         message += (
#             f"Դուք ունեք պարտք՝ {debt}։\n"
#             "Խնդրում ենք հնարավորինս շուտ կատարել պարտքի վճարումը։\n"
#         )

#     if deposit > 0:
#         message += (
#             f"Դուք ունեք կանխավճար՝ {deposit}։\n"
#             "Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
#         )

#     # Payment instructions
#     if debt > 0:
#         message += (
#             "Վճարում կարող եք իրականացնել ինչպես բանկային փոխանցումով, այնպես էլ idram, Easy Wallet, "
#             "Tel Cell, Fast Shift հավելվածներով և Tel Cell, EasyPay, FastShift տերմինալներով։\n"
#             "Բանկային փոխանցման համար:\n"
#             "Հաշվեհամար՝ 1660030213905000\n"
#             "Բանկ՝ էվոկաբանկ\n"
#             "Ստացող՝ «Վերածնունդ թաղամաս համատիրություն»\n"
#             "Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի վճարման կոդը:\n"
#         )

#     # Zero balance case
#     if debt == 0 and deposit == 0:
#         message += "Ձեր հաշվեկշիռը նորմալ է։ Մնում է զրոյական հաշվեկշիռ։\n"

#     return message


# def generate_financial_status_message(code, deposit, debt, apartment, type_of_object, flat_number):
#     """
#     Generate a financial status message for a property.

#     Args:
#         code (str): The property code (e.g., "A-48-2").
#         deposit (float): The deposit amount for the property.
#         debt (float): The debt amount for the property.
#         apartment (str): The apartment location of the property.
#         type_of_object (str): The type of the object (e.g., "Բնակարան").
#         flat_number (str): The flat number associated with the property.

#     Returns:
#         str: A formatted status message.
#     """
#     # Header information
#     message = (
#         f"Գույք համար {code}, որը գտնվում է {apartment}-ում {flat_number}-րդ հարկում ({type_of_object}):\n"
#     )

#     # Handle debt and deposit
#     if debt < 0:
#         message += (
#             f"Դուք ունեք կանխավճար՝ {abs(debt)}։ Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
#         )
#     elif debt > 0:
#         message += (
#             f"Դուք ունեք պարտք՝ {debt}։ Խնդրում ենք հնարավորինս շուտ կատարել վճարումը։\n"
#         )

#     if deposit > 0:
#         message += (
#             f"Դուք ունեք կանխավճար՝ {deposit}։ Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
#         )

#     # Payment instructions
#     if debt > 0:
#         message += (
#             "Վճարում կարող եք իրականացնել ինչպես բանկային փոխանցումով, այնպես էլ idram, Easy Wallet, "
#             "Tel Cell, Fast Shift հավելվածներով և Tel Cell, EasyPay, FastShift տերմինալներով։\n"
#             "Բանկային փոխանցման համար:\n"
#             "Հաշվեհամար՝ 1660030213905000\n"
#             "Բանկ՝ էվոկաբանկ\n"
#             "Ստացող՝ «Վերածնունդ թաղամաս համատիրություն»\n"
#             "Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի վճարման կոդը:\n"
#         )

#     # Zero balance case
#     if debt == 0 and deposit == 0:
#         message += "Ձեր հաշվեկշիռը նորմալ է։ Մնում է զրոյական հաշվեկշիռ։\n"

#     return message



# def generate_financial_status_message2(code, deposit, debt, apartment="N/A", type_of_object="N/A", flat_number="N/A"):
#     """
#     Generate a financial status message for a property.

#     Args:
#         code (str): The property code (e.g., "A-48-2").
#         deposit (float): The deposit amount for the property.
#         debt (float): The debt amount for the property.
#         apartment (str): The apartment location of the property.
#         type_of_object (str): The type of the object (e.g., "Բնակարան").

#     Returns:
#         str: A formatted status message.
#     """
#     if debt > 0:
#         message = (
#             f"Գույք համար {code}, որը գտնվում է <{apartment}>-ում <{type_of_object}> :  <{flat_number}>:\n\n"
#             f"Դուք ունեք պարտք՝ {debt}։ Խնդրում ենք հնարավորինս շուտ կատարել վճարումը։\n"
#             "Վճարում կարող եք իրականացնել ինչպես բանկային փոխանցումով, այնպես էլ idram, Easy Wallet, Tel Cell, Fast Shift հավելվածներով և Tel Cell, EasyPay, FastShift տերմինալներով։\n"
#             "Բանկային փոխանցման համար՝\n"
#             "Հաշվեհամար՝ 1660030213905000\n"
#             "Բանկ՝ էվոկաբանկ\n"
#             "Ստացող՝ «Վերածնունդ թաղամաս համատիրություն»\n"
#             "Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի վճարման կոդը: Օրինակ՝ «A-5520-6» կամ «P-5520-2» կամ «S-5520-212»։\n"
#         )
#     elif deposit > 0:
#         message = (
#             f"Գույք համար {code}, որը գտնվում է <{apartment}>-ում ({type_of_object}):<{flat_number}> \n\n"
#             f"Դուք ունեք կանխավճար՝ {deposit}։ Շնորհակալություն ժամանակին վճարումները կատարելու համար։\n"
#         )

#     else:
#         message = (
#             f"Գույք համար {code}, որը գտնվում է {apartment}-ում ({type_of_object}):\n"
#             f"<{flat_number}>-րդ հարկում:\n\n"
#             "Ձեր հաշվեկշիռը նորմալ է։ Մնում է զրոյական հաշվեկշիռ։\n"
#         )

#     return message