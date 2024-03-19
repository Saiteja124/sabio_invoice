from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for,abort
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
import io
from PIL import Image
import os
# Set your Azure service key and endpoint
# azure_endpoint = 'https://sabio-khub.cognitiveservices.azure.com/'
# azure_key = '519cb0e5e64f4cc591008c74e6bfe5df'

# # Create a FormRecognizerClient
# form_recognizer_credential = AzureKeyCredential(azure_key)
# form_recognizer_client = FormRecognizerClient(azure_endpoint, form_recognizer_credential)

import sys
sys.path.append(r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\ML\Invoice_ocr.py')  # Adjust the path accordingly
sys.path.append(r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\database')
from ML.Invoice_ocr import process_text
from database.create_db import register_user,login_user,user_exists,email_exists

app = Flask(__name__,template_folder=r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\templates')

# def process_pdf(uploaded_file):
    # Convert PDF to images
    # images = convert_from_bytes(uploaded_file.read(), dpi=200, poppler_path=r'C:\Program Files\poppler-23.08.0\Library\bin')

    # # Extract text from each image using Azure Form Recognizer
    # extracted_text = ""
    # for idx, image in enumerate(images):
    #     # Convert the image to grayscale
    #     grayscale_image = image.convert('L')

    #     # Resize the grayscale image to fit within 4MB limit
    #     max_image_size = (2048, 2048)  # Set the maximum image size as needed
    #     grayscale_image.thumbnail(max_image_size, Image.LANCZOS)

    #     # Convert the resized grayscale image to bytes
    #     image_bytes = io.BytesIO()
    #     grayscale_image.save(image_bytes, format='PNG')
    #     image_bytes.seek(0)

    #     # OCR with Azure Form Recognizer
    #     poller = form_recognizer_client.begin_recognize_content(form=image_bytes, content_type="image/png")
    #     form_pages = poller.result()

    #     poller.wait()

        # Extracted text from Form Recognizer response
        # for page in form_pages:
        #     extracted_text += " ".join([line.text for line in page.lines])
extracted_text=""
df = pd.read_csv(r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\Source\project-7-at-2023-10-25-15-38-70d0741e.csv')
df_ = df.drop(labels=[1, 3], axis=0).reset_index(drop=True)
# print(df_)
text1 = df_.text.to_list()
# print(text1)
df_pred = df.loc[[1, 3]].reset_index(drop=True)
text = df_pred.text.to_list()
for tex in text:
    extracted_text += extracted_text+tex
# print(extracted_text)


# registered_users = []

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        # Check if username and email already exist
        username_exist = user_exists(username)
        email_exist = email_exists(email)

        if username_exist and email_exist:
            return jsonify({'registration_success': False, 'username_exists': True, 'email_exists': True})
        elif username_exist:
            return jsonify({'registration_success': False, 'username_exists': True, 'email_exists': False})
        elif email_exist:
            return jsonify({'registration_success': False, 'username_exists': False, 'email_exists': True})
        else:
            # Call the register_user function from create_db.py
            registration_success = register_user(username, email, password)

            if registration_success:
                return jsonify({'registration_success': True})
            else:
                return jsonify({'registration_success': False})

    # Render the registration form for GET requests
    return render_template('registration.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = request.json.get('username')  # Update to use JSON data
        password = request.json.get('password')  # Update to use JSON data

        # Use the login_user function from create_db.py
        if login_user(username, password):
            # Login successful, respond with success status
            return jsonify({'success': True})
        else:
            # Login failed, respond with failure status
            return jsonify({'success': False})

    # Render the login form for GET requests
    return render_template('login.html')


@app.route('/Sabio_use_cases')
def upload_file():
    return render_template('usecases.html')

@app.route('/upload_pdf')
def upload_pdf():
    return render_template('upload_pdf.html')


# Flag to track if PDF has been processed
# pdf_processed = False
@app.route('/process_text', methods=['POST'])
def process_text_route():
    global pdf_processed
    if request.method == 'POST':
        try:
            # Get the input text from the form
            # input_text = request.form['input_text']
            # Get the uploaded PDF file from the request
            # pdf_file = request.files['pdf_file']

            # Create an empty DataFrame for the result
            result_df = pd.DataFrame(columns=['Product_Code', 'Description', 'UPC', 'Quantity', 'Price',
                                              'Line_Amount', 'Invoice_Amount', 'Subtotal', 'Total_Tax',
                                              'Seller_Name', 'Seller_Address', 'Buyer_Name', 'Buyer_Address',
                                              'Invoice_Number', 'Invoice_Date', 'Seller_Phone', 'Seller_Email',
                                              'Po_Number', 'Seller_Website', 'Seller_Fax_Number', 'Shipto_Name',
                                              'Shipto_Address'])

            # Process the input text using your function
            # result_df = process_text(input_text, result_df)
            result_df=process_text(extracted_text, result_df)
            pdf_processed = True

            # Save the result to a CSV file
            result_csv_path = r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\output\processed_result.csv'
            
            result_df.to_csv(result_csv_path, index=False)

            # Assuming 'success' is True if processing is successful
            return jsonify({'success': True})

            

            # Save the result to a CSV file
            # result_csv_path = 'C:\PRASANNA_SABIO_FILES\Invoice_Project\Sabio_Integrating_webpage\output\processed_result.csv'
            
            # result_df.to_csv(result_csv_path, index=False)

            # Save the result to a CSV string
            # result_csv_string = result_df.to_csv(index=False)
            
            # Send the CSV file as an attachment in the response
            # return send_file(result_csv_path, as_attachment=True, download_name='processed_result.csv')

        except Exception as e:
            # Log the error for your reference
            app.logger.error(f"Error processing text: {str(e)}")
            return jsonify({'success': False, 'error': 'An error occurred while processing the text.'})
        
        
# @app.route('/process_specific_fields', methods=['GET', 'POST'])
# def process_specific_fields():
#     if request.method == 'GET':
#         return render_template('specific_fields.html')
#     elif request.method == 'POST':
#         # field1 = request.form.get('fields')
#         # field2 = request.form.get('fields')
#         # fields = [field1, field2]
#         fields_input = request.form.get('fields')
#         fields = [field.strip() for field in fields_input.split(',')]  # Splitting fields by comma

#         # Call specific_fields function to get the DataFrame
#         extracted_df = specific_fields(text, fields)

#         # Write the DataFrame to a CSV file
#         output_file = 'extracted_columns.csv'
#         extracted_df.to_csv(output_file, index=False)
#         return send_file(output_file, as_attachment=True)
# @app.route('/process_specific_fields')
# def process():
#     # return render_template('specific_fields.html')
#     field1 = request.form.get('fields')
#     field2 = request.form.get('fields')
#     fields = [field1,field2]

#     # # Call specific_fields function to get the DataFrame
#     extracted_df = specific_fields(text, fields)
    
#     # # Write the DataFrame to a CSV file
#     output_file = 'extracted_columns.csv'
#     extracted_df.to_csv(output_file, index=False)
#     return send_file(output_file, as_attachment=True)
    # return render_template('specific_fields.html')

# @app.route('/download_csv')
# def download_csv():
#     result_csv_path = 'output/processed_result.csv'
#     return send_file(result_csv_path, as_attachment=True)


@app.route('/download_csv', methods=['GET'])
def download_csv():
    global pdf_processed
    if pdf_processed:
        try:
            result_csv_path = r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\output\processed_result.csv'
            return send_file(result_csv_path, as_attachment=True, download_name='processed_result.csv')
        except Exception as e:
            app.logger.error(f"Error downloading CSV: {str(e)}")
            return jsonify({'success': False, 'error': 'An error occurred while downloading the CSV file.'})
        finally:
            pdf_processed = False  # Reset the flag after downloading
    else:
        return jsonify({'success': False, 'error': 'PDF has not been processed yet.'})
          
# @app.route('/download_csv')
# def download_csv():
#     global pdf_processed
#     result_csv_path = 'C:\PRASANNA_SABIO_FILES\Invoice_Project\Sabio_Integrating_webpage\output\processed_result.csv'
    
#     # Check if the PDF has been processed before allowing download
#     if pdf_processed and os.path.exists(result_csv_path):

#         # Reset the flag after the download
#         pdf_processed = False
#         # If the PDF has been processed and the CSV file exists, send it for download
#         return send_file(result_csv_path, as_attachment=True, download_name='processed_result.csv')
#     else:
#         # If the PDF has not been processed or the CSV file doesn't exist, return an error or redirect as needed
#         abort(404)  # For example, return a 404 error indicating the file is not found

# @app.route('/check_pdf_processed_status', methods=['GET'])
# def check_pdf_processed_status():
#     global pdf_processed
#     # Return the PDF processing status as JSON
#     return jsonify({'pdf_processed': pdf_processed})

if __name__ == '__main__':
    # Use this for development purposes, switch to a production-ready server for deployment
    app.run(debug=True)
