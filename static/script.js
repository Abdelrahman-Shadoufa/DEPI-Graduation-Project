document.getElementById('predict-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    // Collect form data
    const formData = new FormData(e.target);
    const data = {
        Age: parseInt(formData.get('Age')),
        Gender: formData.get('Gender'),
        Tenure: parseInt(formData.get('Tenure')),
        'Usage Frequency': parseInt(formData.get('Usage Frequency')),
        'Support Calls': parseInt(formData.get('Support Calls')),
        'Payment Delay': parseInt(formData.get('Payment Delay')),
        'Total Spend': parseInt(formData.get('Total Spend')),
        'Last Interaction': parseInt(formData.get('Last Interaction')),
        'Subscription Type': formData.get('Subscription Type'),
        'Contract Length': formData.get('Contract Length')
    };

    // Display result div
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'none';
    resultDiv.className = '';

    try {
        // Send POST request to API
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        // Display result
        resultDiv.style.display = 'block';
        if (response.ok) {
            const prediction = result.prediction === 1 ? 'Customer is likely to churn' : 'Customer is not likely to churn';
            resultDiv.className = 'alert alert-success';
            resultDiv.innerHTML = `<strong>Prediction:</strong> ${prediction}`;
        } else {
            resultDiv.className = 'alert alert-danger';
            resultDiv.innerHTML = `<strong>Error:</strong> ${result.error}`;
        }
    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'alert alert-danger';
        resultDiv.innerHTML = `<strong>Error:</strong> Failed to connect to the server.`;
    }
});