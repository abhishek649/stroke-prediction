from flask import Flask, render_template, request
#import jsonify
#import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
#model = pickle.load(open('storke_prediction_model.pkl', 'rb'))
@app.route('/',methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/predictstroke',methods=['GET','POST'])
def predictstroke():
  if request.method == 'POST':
    gender = request.form['gender']
    age = int(request.form['age'])
    hypertension = int(request.form['hyper'])
    heart_disease = int(request.form['heartdisis'])
    ever_married = request.form['maried']
    worktype = request.form['worktype']
    Residence_type = request.form['residenttype']
    avg_glucose_level = float(request.form['avgglucose'])
    bmi = float(request.form['bmi'])
    smoking_status = request.form['smoking']
    my_prediction=predict(gender,age,hypertension,heart_disease,ever_married,Residence_type,avg_glucose_level,bmi,worktype,smoking_status)
    #p_text = np.array2string(my_prediction, precision=2, separator=',',suppress_small=True)
    slength=my_prediction[0]
    if(slength>0):
      return render_template('index.html',prediction_text="You are predicted for Stroke")
    else:
      return render_template('index.html',prediction_text="You are not predicted for Stroke")
    
    


    
def getindex(array,string):
              for i in range(len(array)):
                if array[i] == string:
                    return i
              return None
   
  
def predict(gender,age,hypertension,heart_disease,ever_married,Residence_type,avg_glucose_level,bmi,work_type,smoking_status):
    import numpy as np
    work = ['Never_worked','Private','Self-employed','Self-employed']
    smoking = ['formerly smoked', 'never smoked','smokes']
    with open('model_pickle','rb') as file:
        mp = pickle.load(file)
    x = np.zeros(15)
    if gender == 'male': x[0]=1 
    else:x[0]=0
    x[1]=age
    x[2] = hypertension
    x[3] = heart_disease
    if ever_married == 'Yes':x[4]=1 
    else:x[4]=0
    if Residence_type == 'Urban':x[5]=1 
    else:x[5]=0
    x[6] = avg_glucose_level
    x[7] = bmi
    work_index =getindex(work,work_type)
    smok_index = getindex(smoking,smoking_status)
    if(work_index):x[8+work_index] = 1
    if(smok_index):x[12+smok_index] = 1
    #print(x)
    return mp.predict([x])


if __name__ == "__main__":
    app.run(debug=True, port=8000)