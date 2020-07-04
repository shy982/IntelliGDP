
from flask import Flask,render_template,redirect,url_for,request
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle

app=Flask(__name__, template_folder="templates")
# -------------------------------------
def make_my_prediction(results):
	L = [results['aff'], results['mq'], results['manu'], results['egw'], results['cons'], results['tht'], results['frp'], results['pad'], results['ntp']]
	L = list(map(float, L))
	print("\n\n[ ] L", type(L[0]))
	expected_growth_rate = pd.DataFrame([L])
	print("\n\n[ ] expected grouth expected_growth_rate",expected_growth_rate)
	NN_model = tf.keras.models.load_model('static/my_model.h5')
	pred = NN_model.predict(expected_growth_rate)
	print("[] pred inner", pred)
	return pred[0][0]

# -------------------------------------

def make_my_prediction_for_factors(results):
	GDP=float(results['gdp'])
	filename = r'static/Linear_Regression_model.sav'
	LLR_model = pickle.load(open(filename, 'rb'))
	weights = list(LLR_model.coef_)
	L=["Change Agriculture,forestry & fishing","Change Mining & quarrying","Change Manufacturing","Change Electricity, gas, water supply & other utility services","Change Construction","Change Trade, hotels, transport, communication and services related to broadcasting","Change Financial , real estate & prof servs","Change Public Administration, defence and other services"]
	d={}
	for i in L:
		d[i]=None
	print(d)
	print("GDP=",GDP)
	prev = 14683835
	average_NTT = (629383 + 666741 + 737721	+ 815541 + 877623 + 979909 + 1100747 + 1178298 + 1249229)//9
	GVA = (prev + (GDP*prev)/100) - average_NTT
	GVA = round(GVA)
	prev_stuff = [1940811,354748,2336365,310275,1050533,2627439,2989960,1824473]
	print("Changes Possible to meet your GDP expectations : ")
	for i in range(len(prev_stuff)):
	    arr = prev_stuff[:i]+prev_stuff[i+1:] #Array containing the all the features except the i-th feature 
	    arr_weights = weights[:i]+weights[i+1:]  #Array containing all the weights except the i-th weight
	    summ = sum(np.multiply(arr,arr_weights)) #Element wise product and total sum
	    change = round((GVA - summ)/weights[i])  #applying (y-x)/w
	    print("change feature no. ",i+1,"to : ",change)
	    d[L[i]]=change;
	    if i+1 !=8:
	    	print("\n\t\t\t-----OR------\n")
	    print(d)
	return d


@app.route('/',methods=['GET','POST'])
def demo():
    return render_template("index.html")

@app.route("/gdp", methods=["POST", "GET"])
def calculate_gdp():
	if request.method == 'POST':
		result = request.form
		print("\n\nresutls ", result)
		pred = make_my_prediction(result)

		print("\n\npred ", pred)
		pred = str(pred)
		return render_template("decorated.html", title="first page", prediction=pred)
	return render_template("gdp.html")

@app.route("/factors", methods=["POST", "GET"])
def calculate_gdp1():
	if request.method == 'POST':
		result = request.form
		print("RS", result)
		pred=make_my_prediction_for_factors(result)
		#print("pred", pred)
		return render_template("decorate.html", title="second page", prediction=pred, any_message="Change any of the values to get the entered GDP")
	return render_template("factors.html")
    
@app.route("/random/<v1>/<v2>")
def random_function(v1, v2):
	print("url values = ", v1, v2)


if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)