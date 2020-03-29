import os

from flask import Flask, request, send_file, jsonify
import pdfkit

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)
PDF_TEMP_DIR = ROOT_DIR + '/pdf_temp'

app = Flask(__name__)


def has_pdf(file_name):
    return os.path.isfile(PDF_TEMP_DIR + file_name)


def create_pdf_path():
    idx = 0
    while True:
        if has_pdf(str(idx) + '.pdf'):
            idx += 1
        else:
            break
    
    return PDF_TEMP_DIR + '/' + str(idx) + '.pdf'


@app.route('/wkhtmltopdf/bystr', methods=['POST'])
def download_pdf():
    html_str = request.form['html_str']
    pdf_name = create_pdf_path()
    pdfkit.from_string(html_str, pdf_name)
    try:
        raise Exception
        return send_file(pdf_name, as_attachment=True)
    except:
        return make_response(jsonify(error='server error', 500))
    finally:
        os.remove(pdf_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)

