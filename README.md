# Fruit Freshness Prediction Web App

## Overview
The **Fruit Freshness Prediction Web App** is designed to analyze fruit images, predict their freshness level, estimate expiry, and provide recommendations based on the analysis. The application integrates AI and machine learning to enhance food quality assessment and reduce waste.

## Features
- **Fruit Identification**: Recognizes the type of fruit from an image.
- **Freshness Prediction**: Determines the freshness level and estimates expiry.
- **Recipe Suggestions**: Recommends recipes based on fruit condition.
- **Virtual Fruit Basket**: Stores scanned fruits with their freshness status.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip

### Dependencies
Install the required dependencies using:
```sh
pip install streamlit tensorflow opencv-python numpy pandas
```

## Usage
1. Run the application:
```sh
streamlit run fruit_freshness.py
```
2. Upload an image of the fruit.
3. View the predicted freshness and estimated expiry.
4. Get recipe recommendations based on fruit condition.
5. Store results in the virtual fruit basket.

## File Structure
- `fruit_freshness.py`: Main application script.
- `model.py`: Handles AI model inference for freshness prediction.
- `data_processing.py`: Preprocesses images and extracts relevant features.
- `recipes.py`: Generates recipe recommendations.

## Technologies Used
- **Streamlit**: For interactive UI.
- **TensorFlow**: For deep learning-based freshness prediction.
- **OpenCV**: For image processing.
- **NumPy & Pandas**: For data handling and analysis.

## Future Enhancements
- Improve model accuracy with a larger dataset.
- Add support for multiple image inputs.
- Provide real-time alerts for expiring fruits.
