import os
import pytesseract
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# Tesseract 경로를 환경 변수에서 가져오기
pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', '/usr/bin/tesseract')

brailleMap = {
    'a': '100000', 'b': '101000', 'c': '110000', 'd': '110100', 'e': '100100',
    'f': '111000', 'g': '111100', 'h': '101100', 'i': '011000', 'j': '011100',
    'k': '100010', 'l': '101011', 'm': '110010', 'n': '110110', 'o': '100110',
    'p': '111010', 'q': '111110', 'r': '101110', 's': '011010', 't': '011110',
    'u': '100011', 'v': '101011', 'w': '011101', 'x': '110011', 'y': '110111',
    'z': '100111'
}

def textToBraille(text):
    braille = []
    for char in text.lower():
        braille_code = brailleMap.get(char, '')
        braille.append(braille_code)
    return braille

@app.route('/ocr', methods=['POST'])
def ocr_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        image = Image.open(io.BytesIO(file.read()))
        text = pytesseract.image_to_string(image, lang='eng')

        braille = textToBraille(text)

        return jsonify({
            'originalText': text,
            'brailleBinary': braille
        })
    except pytesseract.TesseractNotFoundError:
        return jsonify({'error': 'Tesseract OCR is not installed or not found in PATH'}), 500
    except Exception as e:
        return jsonify({'error': f'OCR processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)