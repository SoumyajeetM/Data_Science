from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

data = pd.read_csv('Bangalore.csv')
app = Flask(__name__)
pipe=pickle.load(open("BL.pkl", 'rb'))
@app.route('/')
def home():
    #bl 92
    #cn 82
    #dl 57 ridge 67
    #hd 86
    #kk ridge 83 not onehot
    #mb 81

    Metro = ['Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai']
    Bedroom = [1,2,3,4,5,6,7,8,9,10]
    Features=['Resale Available','Gymnasium','Swimming Pool','Landscaped Gardens','Jogging Track','Shopping Mall','Intercom','Sports Facility','Club House','School',
              '24X7 Security','Power Backup','Car Parking','Staff Quarter','Cafeteria','Multipurpose Room','Gas connection','AC','Childrens playarea','Lift Available','Vaastu Compliant','Sofa']
    return render_template('index.html', Metro=Metro, Bedroom=Bedroom, Features=Features)

@app.route('/get_areas/<metro_city>', methods=['GET'])
def get_areas(metro_city):
    areas = get_areas_for_metro(metro_city)
    return jsonify(areas)

# Define a function to extract area/locality data for a given Metro City
def get_areas_for_metro(metro_city):
    if metro_city == 'Bangalore':
        data = pd.read_csv('Bangalore.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("BL.pkl", 'rb'))
    elif metro_city == 'Chennai':
        data = pd.read_csv('Chennai.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("CN.pkl", 'rb'))
    elif metro_city == 'Delhi':
        data = pd.read_csv('Delhi.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("DL.pkl", 'rb'))
    elif metro_city == 'Hyderabad':
        data = pd.read_csv('Hyderabad.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("HD.pkl", 'rb'))
    elif metro_city == 'Kolkata':
        data = pd.read_csv('Kolkata.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("KK.pkl", 'rb'))
    elif metro_city == 'Mumbai':
        data = pd.read_csv('Mumbai.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("MB.pkl", 'rb'))
    else:
        data = pd.read_csv('Bangalore.csv')
        areas = data['Location'].sort_values().unique().tolist()
        pipe = pickle.load(open("BL.pkl", 'rb'))
    #areas = metro_data['Area'].unique().tolist()
    return areas

# Define the MetroAreas dictionary with Metro City as keys and lists of areas/localities as values


@app.route('/predict', methods=['POST'])
def predict():
    try:
        metro_city = request.form.get('Metro')
        if metro_city == 'Bangalore':
            data = pd.read_csv('Bangalore.csv')
        elif metro_city == 'Chennai':
            data = pd.read_csv('Chennai.csv')
        elif metro_city == 'Delhi':
            data = pd.read_csv('Delhi.csv')
        elif metro_city == 'Hyderabad':
            data = pd.read_csv('Hyderabad.csv')
        elif metro_city == 'Kolkata':
            data = pd.read_csv('Kolkata.csv')
        elif metro_city == 'Mumbai':
            data = pd.read_csv('Mumbai.csv')

        Area = request.form.get('Area')
        AreaInt = data[data['Location'] == Area]['Area'].values[0]
        Bedroom = int(request.form.get('Bedroom'))
        selected_features = request.form.getlist('selected_features')
        variable_mapping = {
            'Resale Available': 0,
            'Gymnasium': 0,
            'Swimming Pool': 0,
            'Landscaped Gardens': 0,
            'Jogging Track': 0,
            'Shopping Mall': 0,
            'Intercom': 0,
            'Sports Facility': 0,
            'Club House': 0,
            'School': 0,
            '24X7 Security': 0,
            'Power Backup': 0,
            'Car Parking': 0,
            'Staff Quarter': 0,
            'Cafeteria': 0,
            'Multipurpose Room': 0,
            'Gasconnection': 0,
            'AC': 0,
            'Children'+"'splayarea": 0,
            'Lift Available': 0,
            'Vaastu Compliant': 0,
            'Sofa': 0
        }

        # Set the values to 1 for selected features
        for feature in selected_features:
            if feature in variable_mapping:
                variable_mapping[feature] = 1

        # Check if the form values are not None before converting to float
        if AreaInt is not None and Bedroom is not None:
            try:
                input=pd.DataFrame([[AreaInt, Bedroom]+ list(variable_mapping.values())],
                        columns=['Area','No. of Bedrooms','Resale','Gymnasium','SwimmingPool','LandscapedGardens','JoggingTrack',
                                 'ShoppingMall','Intercom','SportsFacility','ClubHouse','School','24X7Security',
                                 'PowerBackup','CarParking','StaffQuarter','Cafeteria','MultipurposeRoom','Gasconnection',
                                 'AC','Children'"'splayarea",'LiftAvailable','VaastuCompliant','Sofa'])
                prediction = pipe.predict(input)[0]
                return str(prediction)
            except ValueError:
                # Handle the case where the conversion to float fails (e.g., if the input is not a valid number)
                print("Invalid input")
        else:
            # Handle the case where one or more form values are missing
            print("One or more form values are missing")
    except ValueError:
        print("Invalid input for BHK_NO or SQFT")
    return ""

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
