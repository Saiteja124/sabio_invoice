from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for,abort, session, Response
import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
import io
from PIL import Image
import os


import sys
sys.path.append(r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\ML\Invoice_ocr.py')  # Adjust the path accordingly
sys.path.append(r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\database')
from ML.Invoice_ocr import process_text
from database.create_db import register_user,login_user,user_exists,email_exists

app = Flask(__name__,template_folder=r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\templates')


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

def logout():
    # Perform logout actions here, such as clearing session data
    # For example, if you're using session-based authentication:
    session.clear()
    
    # Redirect the user to the login page
    return redirect(url_for('login'))


@app.route('/Sabio_use_cases')
def upload_file():
    return render_template('usecases.html')

@app.route('/upload_pdf')
def upload_pdf():
    return render_template('upload_pdf.html')

df = pd.read_csv('output/processed_result.csv')

# Flag to track if PDF has been processed
# pdf_processed = False
# @app.route('/process_text', methods=['POST'])
# def process_text_route():
#     global pdf_processed
#     if request.method == 'POST':
#         try:
#             # Get the input text from the form
#             # input_text = request.form['input_text']
#             # Get the uploaded PDF file from the request
#             # pdf_file = request.files['pdf_file']

#             # Create an empty DataFrame for the result
#             result_df = pd.DataFrame(columns=['Product_Code', 'Description', 'UPC', 'Quantity', 'Price',
#                                               'Line_Amount', 'Invoice_Amount', 'Subtotal', 'Total_Tax',
#                                               'Seller_Name', 'Seller_Address', 'Buyer_Name', 'Buyer_Address',
#                                               'Invoice_Number', 'Invoice_Date', 'Seller_Phone', 'Seller_Email',
#                                               'Po_Number', 'Seller_Website', 'Seller_Fax_Number', 'Shipto_Name',
#                                               'Shipto_Address'])

#             # Process the input text using your function
#             # result_df = process_text(input_text, result_df)
#             result_df=process_text(extracted_text, result_df)
#             pdf_processed = True

#             # Save the result to a CSV file
#             result_csv_path = r'C:\Users\Sai teja\Desktop\sabio\Sabio_Integrating_webpage\output\processed_result.csv'
            
#             result_df.to_csv(result_csv_path, index=False)

#             # Assuming 'success' is True if processing is successful
#             return jsonify({'success': True})

            

            

#         except Exception as e:
#             # Log the error for your reference
#             app.logger.error(f"Error processing text: {str(e)}")
#             return jsonify({'success': False, 'error': 'An error occurred while processing the text.'})


@app.route('/process_text', methods=['POST'])
def process_text_route():
    if request.method == 'POST':
        try:
            # Get the dynamic text field values from the request
            dynamic_text_fields = request.form.getlist('dynamicText[]')

            # Filter columns based on user-input text fields
            filtered_df = df[dynamic_text_fields]

            # Convert filtered DataFrame to CSV string
            csv_string = filtered_df.to_csv(index=False)

            # Return CSV string as a downloadable file
            return Response(
                csv_string,
                mimetype="text/csv",
                headers={
                    "Content-disposition":
                    "attachment; filename=processed_result_filtered.csv"
                })

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
        
        
# @app.route('/logout', methods=['GET'])
# def logout():
#     # Perform logout actions here, such as clearing session data
#     # For example, if you're using session-based authentication:
#     session.clear()
    
#     # Redirect the user to the login page
#     return redirect(url_for('login'))


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
          


if __name__ == '__main__':
    # Use this for development purposes, switch to a production-ready server for deployment
    app.run(debug=True)
