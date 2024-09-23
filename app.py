from flask import Flask, request
import pandas as pd
from sklearn.decomposition import PCA

app = Flask(__name__)

# Function to load S11 data from CSV
def load_s11_data(csv_file):
    data = pd.read_csv(csv_file)
    # Assuming the first column is frequency and the rest are S11 values
    s11_values = data.iloc[:, 1:].values  # Exclude the frequency column
    return s11_values

# Function to apply PCA and return sugar level based on the PCA result
def apply_pca_and_get_sugar_level(s11_data):
    pca = PCA(n_components=1)  # We want a single principal component
    pca_result = pca.fit_transform(s11_data)
    pca_value = pca_result[0, 0]  # Get the first component (single value)

    # Map PCA value to sugar levels
    if pca_value == 6.3491940523086345:
        return "Sugar Level is 0 mg/dl"
    elif pca_value == 6.3337704684950955:
        return "Sugar Level is 125 mg/dl"
    elif pca_value == 6.3080261359764815:
        return "Sugar Level is 250 mg/dl"
    elif pca_value == 6.2219220940033:
        return "Sugar Level is 500 mg/dl"
    else:
        return "Unknown Sugar Level"

@app.route('/')
def upload_file():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload CSV</title>
    </head>
    <body>
        <h1>Upload a CSV file for S11 Data</h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv" required>
            <br><br>
            <button type="submit">Upload and Process</button>
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def handle_file_upload():
    file = request.files['file']
    file.save('uploaded_file.csv')  # Save uploaded file to Replit's disk

    # Process the uploaded file using your ML code
    s11_data = load_s11_data('uploaded_file.csv')
    sugar_level = apply_pca_and_get_sugar_level(s11_data)

    # Return the result in HTML
    return f'''
    <h1>Sugar Level Detection</h1>
    <p>{sugar_level}</p>
    <br>
    <a href="/">Upload another file</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
