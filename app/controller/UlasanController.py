import joblib
import os
from app.model.ulasan import Ulasan
from app import response, app, db
from flask import jsonify, render_template, request

def index():
    try:
        filter_type = request.args.get('option', 'all')
        print(filter_type)
        
        ulasan = filter(filter_type)
        data = formatarray(ulasan)  # Assuming formatarray is a function to format ulasan data

        label_counts = count_labels()

        return render_template('data-ulasan.html', data=data, label_counts=label_counts)
    
        # ulasan = Ulasan.query.filter_by(predicted_label="Negatif").all()
        # data = formatarray(ulasan)
        # return render_template('data-ulasan.html', data=data)
    except Exception as e:
        print(e)

def filter(filter_type):
    # Get the filter type from query parameter 'filter'

    if filter_type == 'positif':
        ulasan = Ulasan.query.filter_by(predicted_label='Positif').all()
    elif filter_type == 'negatif':
        ulasan = Ulasan.query.filter_by(predicted_label='Negatif').all()
    elif filter_type == 'netral':
        ulasan = Ulasan.query.filter_by(predicted_label='Netral').all()
    else:
        ulasan = Ulasan.query.all() 
    
    return ulasan    # Default to fetching all ulasan if filter is 'all' or unrecognized

def count_labels():
    try:
        # Count the number of positive, negative, and neutral reviews
        positive_count = Ulasan.query.filter_by(predicted_label='Positif').count()
        negative_count = Ulasan.query.filter_by(predicted_label='Negatif').count()
        neutral_count = Ulasan.query.filter_by(predicted_label='Netral').count()

        # Return the counts as a dictionary
        return {
            'positif': positive_count,
            'negatif': negative_count,
            'netral': neutral_count
        }
    except Exception as e:
        print(e)
        return None

def formatarray(data):
    array = []

    for i in data:
        array.append(singleObject(i))

    return array

def singleObject(data):
    data = {
        'id' : data.id,
        'ulasan' : data.ulasan,
        'label' : data.label,
        'predicted_label' : data.predicted_label,
    }

    return data

def predict():
    try:
        ulasan = request.form.get('ulasan')
        predicted_label = preprocessDataAndPredict(ulasan)[0]
        # return response.success(predicted_label, "Berhasil menambahkan data")
        
        
        ulasans = Ulasan(ulasan=ulasan, predicted_label=predicted_label)
        db.session.add(ulasans)
        db.session.commit()
        

        return jsonify({'status': 'success', 'message': 'Ulasan berhasil dikirim'})
    except Exception as e:
        print(e)
        return jsonify({'status': 'error', 'message': 'Terjadi kesalahan'})
    
def preprocessDataAndPredict(Ulasan):
    
    #keep all inputs in array
    test_data = [Ulasan]

    model = os.path.join(app.root_path, '..', 'asset', 'vectorizer.pkl')
    model_nb = os.path.join(app.root_path, '..', 'asset', 'nb_model.pkl')
    
    model_vectorizer = joblib.load(model)
    
    # test_data = ['sangat baik keren sekali kampus ini']
    test_data_transformed = model_vectorizer.transform(test_data)
    #open file
    file = open(model_nb,"rb")
    
    #load trained model
    trained_model = joblib.load(file)
    
    #predict
    prediction = trained_model.predict(test_data_transformed)
    
    return prediction