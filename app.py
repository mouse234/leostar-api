from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/get-activation-code", methods=["POST"])
def get_activation_code():
    data = request.json
    cd_serial = data.get("cd_serial")  # Expected format: "123-456-789-012"
    customer_code = data.get("customer_code")  # Expected format: "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY-Z1234"

    # Ensure cd_serial and customer_code are provided
    if not cd_serial or not customer_code:
        return jsonify({"error": "cd_serial and customer_code are required."}), 400

    # Split the serial and customer codes
    cd_parts = cd_serial.split("-")
    customer_code_parts = customer_code.split("-")

    # Validate the length of the split parts
    if len(cd_parts) != 4 or len(customer_code_parts) != 6:
        return jsonify({"error": "Invalid format for cd_serial or customer_code."}), 400

    # Step 1: Load the form page
    url = "https://www.leostarastrology.com/leostar-code"
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to load the form page."}), 500

    # Step 2: Prepare form data
    form_data = {
        "leostarcodewebenglish1$txtName": "API User",
        "leostarcodewebenglish1$txtEmail": "api@example.com",
        "leostarcodewebenglish1$txtPhoneNumber": "0000000000",
        "leostarcodewebenglish1$cdno1": cd_parts[0],
        "leostarcodewebenglish1$cdno2": cd_parts[1],
        "leostarcodewebenglish1$cdno3": cd_parts[2],
        "leostarcodewebenglish1$cdno4": cd_parts[3],
        "leostarcodewebenglish1$CustomerCodeTxt1": customer_code_parts[0],
        "leostarcodewebenglish1$CustomerCodeTxt2": customer_code_parts[1],
        "leostarcodewebenglish1$CustomerCodeTxt3": customer_code_parts[2],
        "leostarcodewebenglish1$CustomerCodeTxt4": customer_code_parts[3],
        "leostarcodewebenglish1$CustomerCodeTxt5": customer_code_parts[4],
        "leostarcodewebenglish1$CustomerCodeTxt6": customer_code_parts[5],
        "leostarcodewebenglish1$Button1": "GET 30 DIGIT CODE",
    }

    # Step 3: Submit the form
    response = requests.post(url, data=form_data)
    if response.status_code != 200:
        return jsonify({"error": "Failed to submit the form."}), 500

    # Step 4: Parse the response to extract the activation code
    soup = BeautifulSoup(response.text, "html.parser")
    activation_code_element = soup.find("p", {"id": "leostarcodewebenglish1_FptCode"})
    if activation_code_element:
        activation_code = activation_code_element.text.strip()
        return jsonify({"activation_code": activation_code})
    else:
        return jsonify({"error": "Activation code not found."}), 404

if __name__ == "__main__":
    app.run(debug=True)
