from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import io
import os
from werkzeug.utils import secure_filename
import tempfile
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Database setup
DATABASE = 'csv_inspector.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            data TEXT NOT NULL,
            columns TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Read CSV file
            df = pd.read_csv(file)
            
            # Convert DataFrame to JSON for Tabulator
            data = df.to_dict('records')
            columns = [{'title': col, 'field': col, 'headerFilter': True} for col in df.columns]
            
            return jsonify({
                'success': True,
                'data': data,
                'columns': columns,
                'filename': file.filename
            })
        except Exception as e:
            return jsonify({'error': f'Error reading CSV file: {str(e)}'}), 400
    
    return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

@app.route('/save', methods=['POST'])
def save_data():
    try:
        data = request.json
        name = data.get('name', f'Data_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        description = data.get('description', '')
        csv_data = data.get('data', [])
        columns = data.get('columns', [])
        
        if not csv_data:
            return jsonify({'error': 'No data to save'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO saved_data (name, description, data, columns)
            VALUES (?, ?, ?, ?)
        ''', (name, description, json.dumps(csv_data), json.dumps(columns)))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': f'Data saved as "{name}"'})
    except Exception as e:
        return jsonify({'error': f'Error saving data: {str(e)}'}), 500

@app.route('/load/<int:save_id>', methods=['GET'])
def load_data(save_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM saved_data WHERE id = ?', (save_id,))
        saved_item = cursor.fetchone()
        conn.close()
        
        if not saved_item:
            return jsonify({'error': 'Saved data not found'}), 404
        
        return jsonify({
            'success': True,
            'name': saved_item['name'],
            'description': saved_item['description'],
            'data': json.loads(saved_item['data']),
            'columns': json.loads(saved_item['columns']),
            'created_at': saved_item['created_at']
        })
    except Exception as e:
        return jsonify({'error': f'Error loading data: {str(e)}'}), 500

@app.route('/saved', methods=['GET'])
def get_saved_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, description, created_at FROM saved_data ORDER BY created_at DESC')
        saved_items = cursor.fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'saved_data': [dict(item) for item in saved_items]
        })
    except Exception as e:
        return jsonify({'error': f'Error fetching saved data: {str(e)}'}), 500

@app.route('/delete/<int:save_id>', methods=['DELETE'])
def delete_saved_data(save_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM saved_data WHERE id = ?', (save_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Saved data deleted'})
    except Exception as e:
        return jsonify({'error': f'Error deleting saved data: {str(e)}'}), 500

@app.route('/download', methods=['POST'])
def download_file():
    try:
        data = request.json.get('data', [])
        filename = request.json.get('filename', 'edited_data.csv')
        
        if not data:
            return jsonify({'error': 'No data to download'}), 400
        
        # Convert data back to DataFrame
        df = pd.DataFrame(data)
        
        # Create a file-like object in memory
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': f'Error creating download file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
