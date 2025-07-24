from flask import Flask, request, send_file
from pdf417gen import encode, render_image
from PIL import Image
import io

app = Flask(__name__)

@app.route('/barcode', methods=['GET', 'POST'])
def generate_barcode():
    # Accept data from both GET and POST
    if request.method == 'POST':
        data = request.form.get('dl_data')
    else:
        data = request.args.get('data')

    if not data:
        return "Missing 'dl_data' or 'data' parameter", 400

    # ✅ Ensure data starts and ends with double quotes
    if not data.startswith('"'):
        data = '"' + data
    if not data.endswith('"'):
        data = data + '"'

    try:
        # Encode the data to PDF417
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

        # Return the image as a PNG
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
