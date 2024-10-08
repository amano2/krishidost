from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model (you should have saved the model previously using pickle)
with open('cattle_disease_model.pkl', 'rb') as f:
    clf_model = pickle.load(f)

# List of symptoms corresponding to the model
symptoms_list = ['anorexia','abdominal_pain','anaemia','abortions','acetone','aggression','arthrogyposis',
    'ankylosis','anxiety','bellowing','blood_loss','blood_poisoning','blisters','colic','Condemnation_of_livers',
    'coughing','depression','discomfort','dyspnea','dysentery','diarrhoea','dehydration','drooling',
    'dull','decreased_fertility','diffculty_breath','emaciation','encephalitis','fever','facial_paralysis','frothing_of_mouth',
    'frothing','gaseous_stomach','highly_diarrhoea','high_pulse_rate','high_temp','high_proportion','hyperaemia','hydrocephalus',
    'isolation_from_herd','infertility','intermittent_fever','jaundice','ketosis','loss_of_appetite','lameness',
    'lack_of-coordination','lethargy','lacrimation','milk_flakes','milk_watery','milk_clots',
    'mild_diarrhoea','moaning','mucosal_lesions','milk_fever','nausea','nasel_discharges','oedema',
    'pain','painful_tongue','pneumonia','photo_sensitization','quivering_lips','reduction_milk_vields','rapid_breathing',
    'rumenstasis','reduced_rumination','reduced_fertility','reduced_fat','reduces_feed_intake','raised_breathing','stomach_pain',
    'salivation','stillbirths','shallow_breathing','swollen_pharyngeal','swelling','saliva','swollen_tongue',
    'tachycardia','torticollis','udder_swelling','udder_heat','udder_hardeness','udder_redness','udder_pain','unwillingness_to_move',
    'ulcers','vomiting','weight_loss','weakness']

# Route to handle the disease diagnosis request
@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json

    # Extract the symptoms from the request
    cattle_id = data.get('cattleId', '')
    symptoms = data.get('symptoms', {})

    # Convert symptoms into the format expected by the model
    input_symptoms = [0] * len(symptoms_list)
    for i, symptom in enumerate(symptoms_list):
        if symptoms.get(f'symptom{i+1}') in symptoms_list:
            input_symptoms[i] = 1

    # Predict using the pre-trained model
    input_array = np.array([input_symptoms])
    prediction = clf_model.predict(input_array)[0]

    # Return the prediction as a JSON response
    disease_list = ['mastitis','blackleg','bloat','coccidiosis','cryptosporidiosis',
        'displaced_abomasum','gut_worms','listeriosis','liver_fluke','necrotic_enteritis','peri_weaning_diarrhoea',
        ' rift_valley_fever','rumen_acidosis',
        'traumatic_reticulitis','calf_diphtheria','foot_rot','foot_and_mouth','ragwort_poisoning','wooden_tongue','infectious_bovine_rhinotracheitis',
'acetonaemia','fatty_liver_syndrome','calf_pneumonia','schmallen_berg_virus','trypanosomosis','fog_fever']  # Modify based on your model output
    predicted_disease = disease_list[prediction] if prediction < len(disease_list) else 'Unknown'

    return jsonify({
        'cattleId': cattle_id,
        'predictedDisease': predicted_disease
    })

if __name__ == '__main__':
    app.run(debug=True)
