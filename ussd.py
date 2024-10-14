from flask import Flask, request
import africastalking

# Initialize Flask app
app = Flask(__name__)

# Africa's Talking credentials for the sandbox
username = "sandbox"  # For sandbox environment, the username is always 'sandbox'
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Replace with your Africa's Talking API key

# Initialize Africa's Talking
africastalking.initialize(username, api_key)

# Define route to handle USSD requests
@app.route('/ussd', methods=['POST'])
def ussd():
    # Retrieve the incoming POST data from Africa's Talking
    session_id = request.values.get('sessionId', None)
    service_code = request.values.get('serviceCode', None)
    phone_number = request.values.get('phoneNumber', None)  # Phone number sent by simulator
    text = request.values.get('text', '')

    # Log the phone number for debugging (optional)
    print(f"Received USSD request from phone number: {phone_number}")

    # Split the user input into steps based on '*'
    user_input = text.split("*")

    # Initialize response variable
    response = ""

    # USSD logic based on user input
    if text == "":
        # Initial prompt for language selection
        response = "CON Welcome to Poultry Management\n"
        response += "Choose your language:\n"
        response += "1. English\n"
        response += "2. Kiswahili"

    # Step 1: Handle language selection
    elif len(user_input) == 1:
        if user_input[0] == "1":
            response = "CON Enter the hatching date (dd-mm-yyyy):"
        elif user_input[0] == "2":
            response = "CON Weka tarehe ya kuangua (dd-mm-yyyy):"
        else:
            response = "CON Invalid option. Choose your language:\n"
            response += "1. English\n"
            response += "2. Kiswahili"

    # Step 2: Ask for phone number after hatching date is entered
    elif len(user_input) == 2:
        if user_input[0] == "1":
            response = "CON Enter your phone number:"
        elif user_input[0] == "2":
            response = "CON Weka nambari yako ya simu:"
        else:
            response = "CON Invalid option. Please try again."

    # Step 3: Ask if they want to choose Vaccination or Management
    elif len(user_input) == 3:  # Ensure the correct length for this step
        if user_input[0] == "1":
            response = "CON Choose an option:\n"
            response += "1. Vaccination\n"
            response += "2. Management"
        elif user_input[0] == "2":
            response = "CON Chagua chaguo:\n"
            response += "1. Chanjo\n"
            response += "2. Usimamizi"
        else:
            response = "CON Invalid option. Please try again."

    # Step 4a: Vaccination -> Ask for poultry type (Broilers or Layers)
    elif len(user_input) == 4 and user_input[2] == "1":
        if user_input[0] == "1":
            response = "CON Choose poultry type for vaccination:\n"
            response += "1. Broilers\n"
            response += "2. Layers"
        elif user_input[0] == "2":
            response = "CON Chagua aina ya kuku kwa chanjo:\n"
            response += "1. Broilers\n"
            response += "2. Layers"
        else:
            response = "CON Invalid option. Please try again."

    # Step 5a: Display summary for vaccination
    elif len(user_input) == 5 and user_input[2] == "1":
        if user_input[0] == "1":
            poultry_type = "Broilers" if user_input[3] == "1" else "Layers"
            response = f"CON You selected Vaccination for {poultry_type}.\n"
            response += "Send 1 to confirm."
        elif user_input[0] == "2":
            poultry_type = "Broilers" if user_input[3] == "1" else "Layers"
            response = f"CON Umechagua Chanjo kwa {poultry_type}.\n"
            response += "Tuma 1 kuthibitisha."

    # Step 4b: Management -> Ask for poultry type (Broilers or Layers)
    elif len(user_input) == 4 and user_input[2] == "2":
        if user_input[0] == "1":
            response = "CON Choose poultry type for management:\n"
            response += "1. Broilers\n"
            response += "2. Layers"
        elif user_input[0] == "2":
            response = "CON Chagua aina ya kuku kwa usimamizi:\n"
            response += "1. Broilers\n"
            response += "2. Layers"
        else:
            response = "CON Invalid option. Please try again."

    # Step 5b: Display summary for management
    elif len(user_input) == 5 and user_input[2] == "2":
        if user_input[0] == "1":
            poultry_type = "Broilers" if user_input[3] == "1" else "Layers"
            response = f"CON You selected Management for {poultry_type}.\n"
            response += "Send 1 to confirm."
        elif user_input[0] == "2":
            poultry_type = "Broilers" if user_input[3] == "1" else "Layers"
            response = f"CON Umechagua Usimamizi kwa {poultry_type}.\n"
            response += "Tuma 1 kuthibitisha."

    # Step 6: Confirmation and success message
    elif len(user_input) == 6 and user_input[5] == "1":
        if user_input[0] == "1":
            response = "END Your request has been processed successfully."
        elif user_input[0] == "2":
            response = "END Ombi lako limefanikiwa kutumwa."

    # Handle unrecognized input
    else:
        response = "CON Invalid option. Please try again."
        if len(user_input) > 0:
            if user_input[0] == "1":
                response += "\n1. Vaccination\n2. Management"
            elif user_input[0] == "2":
                response += "\n1. Chanjo\n2. Usimamizi"

    return response


# Start the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
