from flask import Flask, render_template, request, jsonify
import os
import base64
import requests
from werkzeug.utils import secure_filename
import json
from config import Config

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
            model="gpt-4o-mini",
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

if __name__ == '__main__':
    print(f"🚀 Starting Flask application on http://{Config.HOST}:{Config.PORT}")
    print(f"📷 Camera recognition app ready!")
    print(f"🔑 Using OpenAI API: {'✅ Configured' if Config.OPENAI_API_KEY else '❌ Not configured'}")
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
