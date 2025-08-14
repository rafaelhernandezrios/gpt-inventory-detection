from flask import Flask, render_template, request, jsonify
import os
import base64
import requests
from werkzeug.utils import secure_filename
import json
from config import Config
import ssl
import ipaddress

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Validate configuration
try:
    Config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please create a .env file with your OpenAI API key")
    exit(1)

def analyze_image_with_gpt(image_base64):
    """
    Analyze image using GPT Vision API to count cans and bottles
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analiza esta imagen y cuenta específicamente cuántas latas y cuántas botellas hay. Responde en formato JSON con esta estructura exacta: {\"latas\": número, \"botellas\": número, \"descripcion\": \"descripción breve de lo que ves\"}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        
        content = response.choices[0].message.content
        
        # Try to parse JSON from the response
        try:
            # Extract JSON from the response (in case there's extra text)
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            parsed_result = json.loads(json_str)
            return parsed_result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            return {
                "latas": 0,
                "botellas": 0,
                "descripcion": content,
                "error": "No se pudo parsear la respuesta como JSON"
            }
            
    except ImportError:
        # Fallback to requests if openai library is not available
        return analyze_image_with_requests(image_base64)
    except Exception as e:
        return {
            "latas": 0,
            "botellas": 0,
            "descripcion": f"Error en la API: {str(e)}",
            "error": True
        }

def analyze_image_with_requests(image_base64):
    """
    Fallback method using requests library
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Config.OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analiza esta imagen y cuenta específicamente cuántas latas y cuántas botellas hay. Responde en formato JSON con esta estructura exacta: {\"latas\": número, \"botellas\": número, \"descripcion\": \"descripción breve de lo que ves\"}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    try:
        response = requests.post(Config.OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        
        # Try to parse JSON from the response
        try:
            # Extract JSON from the response (in case there's extra text)
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            parsed_result = json.loads(json_str)
            return parsed_result
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            return {
                "latas": 0,
                "botellas": 0,
                "descripcion": content,
                "error": "No se pudo parsear la respuesta como JSON"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "latas": 0,
            "botellas": 0,
            "descripcion": f"Error en la API: {str(e)}",
            "error": True
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_camera():
    return render_template('test_camera.html')

@app.route('/upload')
def upload_version():
    return render_template('upload_version.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No se recibió imagen'}), 400
        
        # Remove the data URL prefix to get just the base64 data
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Analyze the image
        result = analyze_image_with_gpt(image_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

def create_self_signed_cert():
    """Create self-signed certificate for HTTPS"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from datetime import datetime, timedelta
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CA"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "GPT Image Recognition"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Save certificate and key
        with open("cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        with open("key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        return True
    except ImportError:
        print("⚠️  cryptography not installed. Using HTTP only.")
        return False

if __name__ == '__main__':
    print("🔍 GPT Image Recognition - HTTPS Version")
    print("=" * 50)
    
    # Try to create SSL certificate
    ssl_available = create_self_signed_cert()
    
    if ssl_available:
        print("✅ SSL certificate created successfully")
        print("🔒 Starting HTTPS server...")
        print(f"🌐 Server will be available at: https://{Config.HOST}:{Config.PORT}")
        print("📱 Open this URL in your browser to use the application")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('cert.pem', 'key.pem')
        
        app.run(
            debug=Config.DEBUG, 
            host=Config.HOST, 
            port=Config.PORT,
            ssl_context=context
        )
    else:
        print("⚠️  Running in HTTP mode (camera may not work)")
        print(f"🌐 Server will be available at: http://{Config.HOST}:{Config.PORT}")
        print("📱 Open this URL in your browser to use the application")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
