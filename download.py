from flask import Flask, render_template, request, send_file
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('download_1.html')


@app.route('/download', methods=['POST'])
def download_excel():
    fileName = request.form['fileName']
    date = request.form['date']
    time = request.form['time']

    # Construct the document name
    documentName = f"{fileName}"

    # Firestore URL
    firestore_url = f"https://storage.googleapis.com/telecom-tower-performance-1.appspot.com/excelFiles/{documentName}/{documentName}.xlsx"

    try:
        # Fetch data from Firestore
        response = requests.get(firestore_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        # Extract URL from response
        excel_url = response.json()["fields"]["url"]["stringValue"]

        # Download Excel file
        excel_response = requests.get(excel_url)
        excel_response.raise_for_status()

        # Return the Excel file as a downloadable attachment
        return send_file(excel_response.content, attachment_filename=f"{fileName}.xlsx", as_attachment=True)

    except requests.exceptions.RequestException as e:
        return f"Error occurred: {e}"


if __name__ == '__main__':
    app.run(debug=True)