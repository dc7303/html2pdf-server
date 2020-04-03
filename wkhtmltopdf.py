import os
import logging
from datetime import datetime

from flask import Flask, request, send_file, jsonify, make_response
import pdfkit

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_TEMP_DIR = '/tmp'
KIT_CONFIG = pdfkit.configuration(wkhtmltopdf=bytes('/usr/local/bin/wkhtmltopdf', 'utf8'))

app = Flask(__name__)


def has_pdf(file_name):
    return os.path.isfile(PDF_TEMP_DIR + file_name)


def create_pdf_path():
    idx = 0
    while True:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        if has_pdf(str(idx) + '.pdf'):
            idx += 1
        else:
            break

    return PDF_TEMP_DIR + '/' + 'file_' + now + '_' + str(idx) + '.pdf'


@app.route('/')
def index():
    return 'Hello world!'


@app.route('/wkhtmltopdf/bystr', methods=['POST'])
def download_pdf():
    html_str = request.form['html_str']
    pdf_path = create_pdf_path()
    pdfkit.from_string(
        html_str,
        pdf_path,
        configuration=KIT_CONFIG,
        options={
            'encoding': 'UTF-8',
            'page-size': 'A4',
        }
    )
    try:
        return send_file(pdf_path, as_attachment=True)
    except:
        return make_response(jsonify(error='server error'), 500)
    finally:
        os.remove(pdf_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)

