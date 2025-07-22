from flask import Flask, request, send_file
from pdf417 import encode, render_image
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>PDF417 Transparent Barcode Generator (via API)</h2>
    <p>Use endpoint like: <code>/barcode?data=YOUR_DATA_HERE</code></p>
    '''

@app.route('/barcode')
def generate_barcode():
    data = request.args.get('data')
    if not data:
        return "Missing 'data' query parameter", 400

    try:
        # Encode data to PDF417 barcode
        codes = encode(data, columns=9, security_level=5)
        img = render_image(codes, scale=5).convert("RGBA")

        # Convert white to transparent
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[:3] == (255, 255, 255):
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)

        # Return image as response
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
