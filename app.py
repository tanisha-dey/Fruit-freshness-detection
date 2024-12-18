from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from PIL import Image
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Initialize the database
def init_db():
    conn = sqlite3.connect('fruits.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fruits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        freshness_score INTEGER,
                        ripeness_stage TEXT,
                        spoilage_date INTEGER,
                        image_path TEXT)''')
    conn.commit()
    conn.close()

# Add a fruit to the database
def add_fruit(name, freshness_score, ripeness_stage, spoilage_date, img_path):
    conn = sqlite3.connect('fruits.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fruits (name, freshness_score, ripeness_stage, spoilage_date, image_path) VALUES (?, ?, ?, ?, ?)",
                   (name, freshness_score, ripeness_stage, spoilage_date, img_path))
    conn.commit()
    conn.close()

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to add a new fruit
@app.route('/api/add-fruit', methods=['POST'])
def add_new_fruit():
    try:
        name = request.form['name']
        freshness_score = int(request.form['freshness_score'])
        ripeness_stage = request.form['ripeness_stage']
        spoilage_date = int(request.form['spoilage_date'])
        file = request.files['image']
        
        # Save the image to the local "images" folder
        if not os.path.exists('images'):
            os.makedirs('images')
        img = Image.open(file.stream)
        img_path = f"images/{name}_{freshness_score}.jpg"
        img.save(img_path)
        
        # Add fruit to the database
        add_fruit(name, freshness_score, ripeness_stage, spoilage_date, img_path)
        
        return jsonify({"success": True, "message": "Fruit added successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Route to view all fruits
@app.route('/api/view-fruits', methods=['GET'])
def view_fruits():
    try:
        conn = sqlite3.connect('fruits.db')
        cursor = conn.cursor()
        
        # Get all fruits from the database
        cursor.execute("SELECT * FROM fruits")
        fruits = cursor.fetchall()
        
        # Create a list of fruits to return as JSON
        fruit_list = []
        for fruit in fruits:
            fruit_list.append({
                "id": fruit[0],
                "name": fruit[1],
                "freshness_score": fruit[2],
                "ripeness_stage": fruit[3],
                "spoilage_date": fruit[4],
                "image_path": f"/images/{os.path.basename(fruit[5])}"
            })
        
        conn.close()
        return jsonify({"success": True, "fruits": fruit_list})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Route to serve fruit images
@app.route('/images/<path:filename>')
def serve_image(filename):
    try:
        return send_from_directory('images', filename)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

# Start the Flask app
if __name__ == '__main__':
    init_db()  # Initialize the database when the server starts
    app.run(debug=True)
