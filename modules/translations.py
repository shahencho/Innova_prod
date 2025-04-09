TRANSLATIONS = {
    # Welcome message shown when the user first enters the bot
    # "welcome_message": "Welcome {name}! I'm your property management assistant. To get started, please share your phone number.",
    
    # "welcome_message": "Ողջույն {name}! Ես Իննովա Մենեջմենթի բոտն եմ։ Կօգնեմ Ձեզ ստանալ հետևյալ տեղեկությունները՝ համատիրության ընթացիկ պարտք կամ կանխավճար, վճարումների պատմություն, և այլ օգտակար ինֆորմացիա համատիրության աշխատանքների մասին։ Սկսելու համար՝ սեղմեք ներքևի «📱 Կիսվել հեռախոսահամարով» կոճակը՝ ձեր Telegram-ում գրանցված համարը ուղարկելու համար։ Մենք կստուգենք այս համարը՝ համապատասխանեցնելով այն Իննովա Մենեջմենթ-ի գրանցամատյանի տվյալների հետ։ Եթե համարը գրանցված է, Դուք կկարողանաք օգտագործել բոտի հնարավորությունները։ Նշում․ Այս պահին բոտը հասանելի է միայն այն օգտատերերին, որոնց հեռախոսահամարը գրանցված է համատիրության գրանցամատյանում։"


    
    "welcome_message": 
    (
        "Ողջույն {name}!\n\n"
        "Ես Իննովա Մենեջմենթի բոտն եմ։ Կօգնեմ Ձեզ ստանալ հետևյալ տեղեկությունները՝\n"
        "- Համատիրության ընթացիկ պարտք կամ կանխավճար\n"
        "- Վճարումների պատմություն\n"
        "- Այլ օգտակար ինֆորմացիա համատիրության աշխատանքների մասին։\n\n"
        "Սկսելու համար՝ սեղմեք ներքևի «📱 Կիսվել հեռախոսահամարով» կոճակը՝ Ձեր Telegram-ում գրանցված համարը ուղարկելու համար։\n\n"
        "Մենք կստուգենք այս համարը՝ համեմատելով այն համատիրության գրանցամատյանի տվյալների հետ։\n\n"
        "Եթե համարը գրանցված է, ապա Դուք կկարողանաք օգտագործել բոտի հնարավորությունները։"
    ),
    

    # Prompt for entering mobile number in a valid format
    # "ask_mobile_number": (
    #     "Խնդրում ենք մուտքագրեք ձեր հեռախոսահամարը, որը գրանցված է համատիրության գրանցամատյանում այս ֆորմատով՝ "
    #     "+374xxxxxxxx կամ 0xxxxxxxx to test use - <37491995901> <37494777513> <37455024479> <37494555585> "
    # ),
    "ask_mobile_number": "👇👇👇",
    "share_phone": "📱 Կիսվել հեռախոսահամարով",
    # Message when displaying found objects assigned to the user
    "found_objects": "{mobile_number_param} հեռախոսահամարին կցված է հետևյալ գույքը։",

    "select_object_to_see_history": "Ընտրեք գույքը՝ վճարումների պատմությունը դիտելու համար։",

    # Button text for changing associated mobile number
    "change_mobile": "Դիտարկել այլ հեռախոսահամարին կցած գույքի մասին ինֆորմացիա։",
    # Error message when failing to fetch property details
    "fetch_details_failed": "Չհաջողվեց ստանալ գույքի մանրամասները։ Խնդրում ենք փորձել ավելի ուշ։",
    # Header for payment history
    "payment_history": "Վճարումների պատմություն {code}-ի համար:\n{history}",
    # Message when no transactions are found for an object
    "no_transactions": "{code}-ի համար վճարումներ չեն գտնվել։",
    # Question asking the user if they want to see payment details
    "ask_to_view_details": "Եթե ցանկանում եք տեսնել վճարման մանրամասները, սեղմեք մենյուի համապատասխան կոճակը։",
    # Prompt to enter a new mobile number
    # "enter_new_mobile": (
    #     "Խնդրում ենք մուտքագրել Ձեր նոր հեռախոսահամարը հետևյալ ֆորմատով՝ +374xxxxxxxx կամ 0xxxxxxxx։ "
    #     "to test use - <37491995901> <37494777513> <37455024479> <37494555585>"
    # ),

    "enter_new_mobile": (
        "Խնդրում ենք մուտքագրել Ձեր նոր հեռախոսահամարը հետևյալ ֆորմատով՝ +374xxxxxxxx կամ 0xxxxxxxx։ "        
    ),

    # Message confirming the found mobile number and associated properties
    "mobile_saved_in_db_found": "Գտանք Ձեր հեռախոսահամարին կցված գույք։ Վերջին անգամ օգտագործված հեռախոսահամարը` ",
    # Prompt to choose a flat building
    "choose_flat_building": (
        "Դուք ընտրել եք ԲՆԱԿԱՐԱՆ, ընտրեք շենքը "
        "(ճշգրիտ հասցեն կարող եք ճշտել սեփականության վկայականից)"
    ),
    # Prompt to enter a flat number
    "enter_flat_number": (
        "Դուք ընտրեցիք {building} շենքը։ Ընտրեք բնակարանը կամ միավորի համարը "
        "(ճշգրիտ հասցեն կարող եք ճշտել սեփականության վկայականից)"
    ),
    # Prompt to choose a public space building
    "choose_public_space_building": (
        "Դուք ընտրել եք \"Հասարակական Տարածք\", ընտրեք շենքը "
        "(ճշգրիտ հասցեն կարող եք ճշտել սեփականության վկայականից)"
    ),
    # Prompt to enter a public space ID
    "enter_public_space_id": (
        "Դուք ընտրեցիք {building} շենքը։ Ընտրեք միավորի համարը "
        "(ճշգրիտ հասցեն կարող եք ճշտել սեփականության վկայականից)"
    ),
    # Prompt to choose a parking building
    "choose_parking_building": (
        "Դուք ընտրել եք \"Կայանատեղի\", ընտրեք շենքը "
        "(ճշգրիտ հասցեն կարող եք ճշտել սեփականության վկայականից)"
    ),
    # Prompt to enter a parking ID
    "enter_parking_id": (
        "Դուք ընտրեցիք {building} շենքը։ Ընտրեք կայանատեղի համարը "
        "(ճշգրիտ հասցեն կարող եք ճշտել սեփականության վկայականից)"
    ),
    # Mobile response header when properties are found
    "mobile_response_header": "Գտանք մի քանի գույք կցած այս համարին՝",
    # Mobile response for each object
    "mobile_response_object": "{index}. {code} ({type})։ Պարտքը կազմում է {debt} դրամ",

    "found_properties": "Գտնվել են հետևյալ գույքերը՝ {properties}",

    "case_no_debt_no_deposit": (
        "{code} ՊԱՐՏՔԸ հավասար է 0-ի, կանխավճարն էլ հավասար է 0-ի, ինչը նշանակում է, որ բոլոր վճարումները ժամանակին են։ "
        "Շնորհակալություն Ձեր պարտաճանաչության համար։"
    ),
    "case_no_debt_with_deposit": (
        "{code} Դուք ունեք կանխավճար, գումարը՝ {deposit} դրամ։ "
        "Շնորհակալություն ժամանակին վճարումները կատարելու և մեզ վստահելով՝ կանխավճար վճարելու համար։"
    ),
    "case_debt_and_deposit": (
        "{code} Դուք ունեք կանխավճար՝ {deposit}, և պարտք՝ {debt}։ "
        "Ցանկանու՞մ եք տեսնել մանրամասները (պարտք/կանխավճար)։"
    ),
    "mobile_number_saved": "Ձեր հեռախոսահամարը {new_mobile_number} պահպանվել է։",
    "yes_show_objects": "Ցույց տալ իմ գույքի մանրամասները",
    "case_debt_no_deposit": (
        "Դուք ունեք պարտք, պարտքի գումարը՝ {debt} դրամ։ Խնդրում ենք հնարավորինս շուտ կատարել վճարումը։\n"
        "Վճարում կարող եք իրականացնել ինչպես բանկային փոխանցումով, այնպես էլ idram, Easy Wallet, Tel Cell, Fast Shift հավելվածներով "
        "և Tel Cell, EasyPay, FastShift տերմինալներով։\n"
        "Բանկային փոխանցման համար՝\n"
        "Հաշվեհամար՝ 1660030213905000\n"
        "Բանկ՝ էվոկաբանկ\n"
        "Ստացող՝ «Վերածնունդ թաղամաս համատիրություն»\n"
        "Վճարում կատարելիս նպատակը դաշտում նշել տվյալ գույքի վճարման կոդը:\n"
        "Օրինակ՝ «A-5520-6», «P-5520-2» կամ «S-5520-212»։\n"
        "\nԱյս գույքի վճարման կոդն է՝ {code}"
    ),

    # New Values (from Original Version)
    # "back_to_objects": "Վերադառնալ",
    "no_mobile_number_linked": "no_mobile_number_linked",
    "Refresh": "Թարմացնել",
    "Back1": "Վերադառնալ",
    "Blady": "Վերադառնալ.",
    # "choose_action": "choose_action",
    "invalid_mobile_format": "invalid_mobile_format",

    "unknown_command": "Ներեցեք, չեմ հասկանում ինչ հարցում եք կատարում, Խնդրում եմ կրկին փորձեք` ընտրելով համապատասխան կոճակը",

    "session_lost": "Թարմացնում եմ կապը սերվերի հետ",

   
    "View_Report": "Տեսնել հաշվետությունը",


    
    # "valid_not_registered_in_API": """Այս հեռ․ համարով գրանցված գույք չի գտնվել:
    # Խնդրում ենք մուտքագրեք ձեր հեռախոսահամարը, որը գրանցված է համատիրության գրանցամատյանում այս ֆորմատով՝
    # +374xxxxxxxx կամ 0xxxxxxxx""",


    "valid_not_registered_in_API": (
        "Հարգելի օգտատեր, համատիրության գրանցամատյանում այս հեռախոսահամարով գրանցված գույք չի գտնվել։ "
        "Ձեր տելեգրամյան հաշվի հեռախոսահամարը պետք է համընկնի համատիրության գրանցամատյանում գրանցված հեռախոսահամարի հետ։ "
        "Եթե կարծում եք սխալմունք կա, և Դուք եք սեփականատերը և պետք է Ձեր հեռախոսահամարը գրանցված լինի գրանցամատյանում՝ "
        "խնդրում ենք նամակ գրեք veratsnund@innovapm.am հասցեին՝ նկարագրելով խնդիրը։\n\n"
        "Շնորհակալություն։"
    ),


    
    
    "property_details": "Սեփականության մանրամասներ",
    "property_type": "Գույքի տեսակ՝",
    "property_code": "Վճարման կոդ՝",
    "property_address": "Հասցե՝",
    "property_number": "Համար",
    

    "not_valid_format":   "Խնդրում ենք մուտքագրել Ձեր նոր հեռախոսահամարը հետևյալ ֆորմատով՝ +374xxxxxxxx կամ 0xxxxxxxx",
    
    "back_to_main_menu1": "Սեղմեք 'Վերադառնալ' կոճակը:"
}
