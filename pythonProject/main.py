from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('train.csv')
pipe = pickle.load(open("RandomForestModel.pkl",'rb'))

@app.route('/')
def home():
    POSTED_BY = sorted(data['POSTED_BY'].unique())
    BHK_NO = sorted(data['BHK_NO.'].unique())
    return render_template('index.html', POSTED_BY=POSTED_BY, BHK_NO=BHK_NO)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        print("1")
        POSTED_BY = request.form.get('POSTED_BY')
        BHK_NO_int = int(request.form.get('BHK_NO'))
        SQFT_str = float(request.form.get('SQFT'))
        print(POSTED_BY, BHK_NO_int, SQFT_str)

        # Check if the form values are not None before converting to float
        if BHK_NO_int is not None and SQFT_str is not None:
            try:
                print("2")

                input=pd.DataFrame([[POSTED_BY,SQFT_str, BHK_NO_int]],columns=['POSTED_BY','SQUARE_FT','BHK_NO.'])
                print(f"POSTED_BY: {POSTED_BY}, BHK_NO: {BHK_NO_int}, SQFT: {SQFT_str}")
                prediction=pipe.predict(input)[0]
                print("Done")
                return str(prediction)
            except ValueError:
                # Handle the case where the conversion to float fails (e.g., if the input is not a valid number)

                print("Invalid input for BHK_NO or SQFT")
        else:
            # Handle the case where one or more form values are missing
            print("3")
            print("One or more form values are missing")
    except ValueError:
        print("Invalid input for BHK_NO or SQFT")
    return ""

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
