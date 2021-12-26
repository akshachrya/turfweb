from flask import Flask,render_template,request,jsonify
from turf import turf_analysis
import pandas as pd
import json

data="TURF_Level1.csv"


app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def main():
	data=pd.read_csv('TURF_Level1.csv')
	dataset = pd.DataFrame(data)
	column=list(dataset.columns)
	newdataset=dataset.dropna(how='all').replace('yes',1).fillna(0)
	totalrespon,columnssize=newdataset.shape

	#How much configuration can we make
	subset_size=columnssize
	subsetarray=[]
	for i in range(1,subset_size+1):
		subsetarray.append(i)


	if request.method=='POST':
		reqdata=request.data
		reqdata=json.loads(reqdata)
		print(reqdata)
		result={}
		subset_size=int(reqdata['subsetsize'])
		columns=reqdata['topic']
		main=turf_analysis(newdataset[columns], subset_size=subset_size, objective=[0,1],product_labels=column,columns=columns)
		a=main[0]
		b=main[1]
		table=pd.DataFrame(a).T
		table.columns=['Configurations',
		'Frequency']
		table['Configurations']=table['Configurations'].astype(str)
		table['Frequency_per']=table['Frequency']/len(newdataset)*100
		table=table.sort_values(by ='Frequency',ascending=False)
		result['frequencytable']=table.to_dict('records')
		
		table1=pd.DataFrame(b).T
		table1.columns=['Configurations','Reach']
		table1['Configurations']=table1['Configurations'].astype(str)
		table1['Reach_per']=table1['Reach']/len(newdataset)*100
		table1=table1.sort_values(by ='Reach',ascending=False)
		result['reachtable']=table1.to_dict('records')

		return json.dumps(result)

	else:
		return render_template('plot.html',columns=column)

if __name__=="__main__":
    app.run(debug=True)
