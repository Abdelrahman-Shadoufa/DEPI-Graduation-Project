from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

app = Flask(__name__)

# Load the pre-trained model
try:
    with open('knn_model.pkl', 'rb') as file:
        model = pickle.load(file)
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Define the expected columns (16 features)
columns = [
    'Age', 'Tenure', 'Usage Frequency', 'Support Calls', 
    'Payment Delay', 'Total Spend', 'Last Interaction', 
    'Subscription Type_Basic', 'Subscription Type_Premium', 'Subscription Type_Standard',
    'Contract Length_Annual', 'Contract Length_Monthly', 'Contract Length_Quarterly',
    'Gender_Male', 'Gender_Female', 'Placeholder_Feature'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        required_fields = [
            'Age', 'Gender', 'Tenure', 'Usage Frequency', 'Support Calls',
            'Payment Delay', 'Total Spend', 'Last Interaction', 'Subscription Type',
            'Contract Length'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        subscription_type = data['Subscription Type']
        contract_length = data['Contract Length']

        subscription_basic = 1 if subscription_type == 'Basic' else 0
        subscription_premium = 1 if subscription_type == 'Premium' else 0
        subscription_standard = 1 if subscription_type == 'Standard' else 0

        if subscription_type not in ['Basic', 'Premium', 'Standard']:
            return jsonify({'error': 'Invalid Subscription Type. Must be Basic, Premium, or Standard'}), 400

        contract_annual = 1 if contract_length == 'Annual' else 0
        contract_monthly = 1 if contract_length == 'Monthly' else 0
        contract_quarterly = 1 if contract_length == 'Quarterly' else 0

        if contract_length not in ['Annual', 'Monthly', 'Quarterly']:
            return jsonify({'error': 'Invalid Contract Length. Must be Annual, Monthly, or Quarterly'}), 400

        gender_male = 1 if data['Gender'] == 'Male' else 0
        gender_female = 1 if data['Gender'] == 'Female' else 0

        if data['Gender'] not in ['Male', 'Female']:
            return jsonify({'error': 'Invalid Gender. Must be Male or Female'}), 400

        input_data = pd.DataFrame([[
            data['Age'], 
            data['Tenure'], 
            data['Usage Frequency'], 
            data['Support Calls'], 
            data['Payment Delay'], 
            data['Total Spend'], 
            data['Last Interaction'], 
            subscription_basic, 
            subscription_premium, 
            subscription_standard, 
            contract_annual, 
            contract_monthly, 
            contract_quarterly,
            gender_male, 
            gender_female, 
            0  # Placeholder_Feature (replace with actual feature)
        ]], columns=columns)

        prediction = model.predict(input_data)[0]

        return jsonify({
            'prediction': int(prediction),
            'message': 'Prediction successful'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)