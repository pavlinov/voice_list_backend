from flask import Flask, request, jsonify, render_template_string, render_template, abort
from flask_cors import CORS
import re
import hashlib

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:8080", "http://localhost", "http://localhost:80"])

    # All your previous code (routers and functions) goes here
    def is_email_valid(email):
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return email_regex.match(email)

    def generate_api_key(email):
        secret_key = "your_secret_key"
        api_key = hashlib.sha256((email + secret_key).encode()).hexdigest()
        return api_key

    def check_authorization(api_key, email):
        return api_key == generate_api_key(email)

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data.get('email')

        if not is_email_valid(email):
            return jsonify({"error": "Invalid email address"}), 400

        if email != 'john.doe@example.com':
            return jsonify({'error': "Wrong user email"}), 401

        api_key = generate_api_key(email)
        return jsonify({"api_key": api_key})

    @app.route('/generate', methods=['POST'])
    def generate_html():
        data = request.get_json()

        full_name = data.get('full_name')
        title = data.get('title')
        company = data.get('company')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        api_key = data.get('api_key')
        selected_type = data.get('selected_type') if (data.get('selected_type') in ['type_1', 'type_2']) else 'test'

        if not is_email_valid(email):
            return jsonify({"error": "Invalid email address"}), 400

        if not check_authorization(api_key, email):
            return jsonify({"error": "Unauthorized"}), 401

        rendered_html = render_template(f'{selected_type}.html',
                                        full_name=full_name,
                                        title=title,
                                        company=company,
                                        email=email,
                                        phone=phone,
                                        address=address)

        return jsonify({"html": rendered_html})

    return app

app = create_app()



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


