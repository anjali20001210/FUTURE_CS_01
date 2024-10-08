from flask import Flask, request, redirect, url_for, flash, render_template
import qrcode
import pyotp
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = "2factorauth"

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_data = None
    if request.method == 'POST':
        otp = request.form['otp']
        # Generate a new key for each submission
        key_gen = pyotp.random_base32()
        totp = pyotp.TOTP(key_gen)

        if totp.verify(otp):
            flash("OTP is Correct", "success")
            return redirect(url_for('success'))
        else:
            flash("Invalid OTP", "danger")

    # Generate the QR code each time the page loads
    key_gen = pyotp.random_base32()  # You may want to persist this key for real-world use
    totp = pyotp.TOTP(key_gen)
    qr = totp.provisioning_uri(name="2fa", issuer_name="Hareshwhar")

    qr_image = qrcode.make(qr)
    buffer = BytesIO()
    qr_image.save(buffer)
    qr_data = base64.b64encode(buffer.getvalue()).decode()

    return render_template('index.html', qr_data=qr_data)

@app.route('/success')
def success():
    return "OTP verified successfully!"

if __name__ == '__main__':
    app.run(debug=True)
