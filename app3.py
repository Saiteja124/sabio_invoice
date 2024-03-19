# import os
# import csv
# from flask import Flask, render_template, request, redirect, url_for
# import pytesseract
# from pdf2image import convert_from_path
# import cv2
# import numpy as np
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['ALLOWED_EXTENSIONS'] = ['pdf']

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         # Handle file upload
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)

#             # Perform OCR on the PDF file
#             images = convert_from_path(file_path, poppler_path=r'C:\Program Files\poppler-23.08.0\Library\bin')
#             text = ''
#             for image in images:
#                 text += pytesseract.image_to_string(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

#             # Render the PDF on the canvas
#             pdf_image = cv2.imread(file_path)
#             _, pdf_data = cv2.imencode('.png', pdf_image)
#             pdf_base64 = 'data:image/png;base64,' + pdf_data.tostring().decode('utf-8')

#             return render_template('boundary.html', pdf_text=text, pdf_base64=pdf_base64)

#     return render_template('boundary.html')

# @app.route('/save_coordinates', methods=['POST'])
# def save_coordinates():
#     column_names = request.form.getlist('columnName[]')
#     coordinates = request.form.getlist('coordinates[]')

#     # Save data to a CSV file
#     csv_file = 'coordinates.csv'
#     with open(csv_file, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Column Name', 'Coordinates'])
#         for name, coord in zip(column_names, coordinates):
#             writer.writerow([name, coord])

#     return 'Coordinates saved successfully'

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import csv
import base64
from flask import Flask, render_template, request, redirect, url_for
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['pdf']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Perform OCR on the PDF file
            images = convert_from_path(file_path, poppler_path=r'C:\Program Files\poppler-23.08.0\Library\bin')
            text = ''
            for image in images:
                text += pytesseract.image_to_string(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))

            # Render the first page of the PDF on the canvas
            pdf_image = cv2.cvtColor(np.array(images[0]), cv2.COLOR_RGB2BGR)
            _, pdf_data = cv2.imencode('.png', pdf_image)
            pdf_base64 = 'data:image/png;base64,' + base64.b64encode(pdf_data).decode('utf-8')

            return render_template('boundary1.html', pdf_text=text, pdf_base64=pdf_base64)

    return render_template('boundary1.html')

@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    column_names = request.form.getlist('columnName[]')
    coordinates = request.form.getlist('coordinates[]')

    # Save data to a CSV file
    csv_file = 'coordinates.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Column Name', 'Coordinates'])
        for name, coord in zip(column_names, coordinates):
            writer.writerow([name, coord])

    return 'Coordinates saved successfully'

if __name__ == '__main__':
    app.run(debug=True)