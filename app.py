from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/get-activation-code", methods=["POST"])
def get_activation_code():
    data = request.json
    cd_serial = data.get("cd_serial")  # Format: "123-456-789-012"
    customer_code = data.get("customer_code")  # Format: "ABCDE-FGHIJ-KLMNO-PQRST-UVWXY-Z1234"

    # Step 1: Load the form page to extract hidden fields
    url = "https://www.leostarastrology.com/leostar-code"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract hidden fields
    viewstate = soup.find("input", {"id": "__VIEWSTATE"})["value"]
    event_validation = soup.find("input", {"id": "__EVENTVALIDATION"})["value"]
    viewstate_generator = soup.find("input", {"id": "__VIEWSTATEGENERATOR"})["value"]

    # Step 2: Prepare form data
    form_data = {
        "__VIEWSTATE": viewstate,
        "__EVENTVALIDATION": event_validation,
        "__VIEWSTATEGENERATOR": viewstate_generator,
        "leostarcodewebenglish1$txtName": "API User",
        "leostarcodewebenglish1$txtEmail": "api@example.com",
        "leostarcodewebenglish1$txtPhoneNumber": "0000000000",
        "leostarcodewebenglish1$cdno1": cd_serial.split("-")[0],
        "leostarcodewebenglish1$cdno2": cd_serial.split("-")[1],
        "leostarcodewebenglish1$cdno3": cd_serial.split("-")[2],
        "leostarcodewebenglish1$cdno4": cd_serial.split("-")[3],
        "leostarcodewebenglish1$CustomerCodeTxt1": customer_code.split("-")[0],
        "leostarcodewebenglish1$CustomerCodeTxt2": customer_code.split("-")[1],
        "leostarcodewebenglish1$CustomerCodeTxt3": customer_code.split("-")[2],
        "leostarcodewebenglish1$CustomerCodeTxt4": customer_code.split("-")[3],
        "leostarcodewebenglish1$CustomerCodeTxt5": customer_code.split("-")[4],
        "leostarcodewebenglish1$CustomerCodeTxt6": customer_code.split("-")[5],
        "leostarcodewebenglish1$Button1": "GET 30 DIGIT CODE",
    }

    # Step 3: Submit the form
    response = requests.post(url, data=form_data)

    # Step 4: Parse the response to extract the activation code
    soup = BeautifulSoup(response.text, "html.parser")
    activation_code = soup.find("p", {"id": "leostarcodewebenglish1_FptCode"}).text.strip()

    return jsonify({"activation_code": activation_code})

if __name__ == "__main__":
    app.run(debug=True)
