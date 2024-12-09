import streamlit as st
import requests
from PIL import Image

# Streamlit UI for adding fruit
st.title("Fruit Basket")

# Get fruit details
name = st.text_input("Fruit Name")
freshness_score = st.slider("Freshness Score", 1, 10)
ripeness_stage = st.selectbox("Ripeness Stage", ["Unripe", "Ripe", "Overripe"])
spoilage_date = st.number_input("Spoilage Date (in days)", min_value=1, max_value=365)

# Upload an image of the fruit
uploaded_image = st.file_uploader("Upload Fruit Image", type=["jpg", "png", "jpeg"])

# Add fruit button
if st.button("Add Fruit"):
    if uploaded_image is not None and name and freshness_score and ripeness_stage and spoilage_date:
        # Prepare the data to send to the backend
        files = {'image': uploaded_image}
        data = {
            'name': name,
            'freshness_score': freshness_score,
            'ripeness_stage': ripeness_stage,
            'spoilage_date': spoilage_date
        }
        
        # Send data to Flask backend
        response = requests.post("http://127.0.0.1:5000/api/add-fruit", files=files, data=data)
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                st.success("Fruit added successfully")
            else:
                st.error(f"Failed to add fruit: {result['message']}")
        else:
            st.error(f"Failed to connect to server: {response.status_code}")
    else:
        st.error("Please fill in all fields and upload an image")

# View Fruits button to display the entered fruits
if st.button("View All Fruits"):
    # Send GET request to the Flask backend to get the list of fruits
    response = requests.get("http://127.0.0.1:5000/api/view-fruits")
    
    if response.status_code == 200:
        result = response.json()
        if result["success"]:
            fruits = result["fruits"]
            if fruits:
                # Display fruits in a grid layout similar to Amazon's product listing
                cols = st.columns(3)  # 3 columns for listing items like Amazon
                
                for i, fruit in enumerate(fruits):
                    col = cols[i % 3]  # To cycle through columns for each fruit
                    
                    with col:
                        # Display fruit details
                        st.subheader(fruit['name'])
                        st.text(f"Freshness: {fruit['freshness_score']}/10")
                        st.text(f"Ripeness: {fruit['ripeness_stage']}")
                        st.text(f"Spoilage Date: {fruit['spoilage_date']} days")
                        
                        # Display fruit image, resized to a smaller size
                        st.image(fruit["image_path"], width=150)
            else:
                st.info("No fruits found!")
        else:
            st.error(f"Failed to load fruits: {result['message']}")
    else:
        st.error(f"Failed to connect to server: {response.status_code}")
