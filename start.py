from flask import Flask, request, send_file
import pdfkit

app = Flask(__name__)

@app.route('/')
def index():
    return 'hello, world'

@app.route('/downloadpdf', methods=['POST'])
def download_pdf():
    html_str = request.form['html_str']
    pdfkit.from_string(html_str, 'result.pdf')
    return send_file('result.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

