import json
import csv  
import sys
from datetime import datetime

header = ['Layers', 'PadToPad', 'PadToTrack', 'TrackToTrack','MinLineWidth','TrackToRegion']
MaterialStackup = ['Type','Name','Thickness (mm)','Material','Color','DielectricConstant']
header2=['DesignRules']
header3=['MaterialStackup']
header4=['GeneralSpecs']
header5=['Dimentions']
header6=['LayerNumber','BoardThickness','Finish','ImpedanceControlled','Castellated']

gbrjob = sys.argv[1]
print(gbrjob)

fj = open(gbrjob)
# returns JSON object as
# a dictionary
data = json.load(fj)
 
# Iterating through the json
# list

name = ["Name",data["GeneralSpecs"]["ProjectId"]["Name"]]
GUID = ["GUID",data["GeneralSpecs"]["ProjectId"]["GUID"]]
Revision = ["Rev",data["GeneralSpecs"]["ProjectId"]["Revision"]]

date_time_str= data["Header"]["CreationDate"]
time_formated= datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S%z')
time_reformated = str(time_formated.day)+"/"+str(time_formated.month)+"/"+str(time_formated.year)

print(time_reformated)

Date = ["Date",time_reformated]


Dimention = [data["GeneralSpecs"]["Size"]["X"],data["GeneralSpecs"]["Size"]["Y"]]
ci = False
cas = False
try:
	if data["GeneralSpecs"]["ImpedanceControlled"]:
		ci=True
except Exception as e:
	print(e)

try:
    if data["GeneralSpecs"]["Castellated"]:
        cas=True
except Exception as e:
    print(e)



GeneralSpecs= [data["GeneralSpecs"]["LayerNumber"],data["GeneralSpecs"]["BoardThickness"],data["GeneralSpecs"]["Finish"],ci,cas]


with open('config_electrical.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow(name)
    writer.writerow(Date)
    writer.writerow(GUID)
    writer.writerow(Revision)
    writer.writerow('')
    writer.writerow(header6)
    writer.writerow(GeneralSpecs)
    writer.writerow('')
    writer.writerow(header5)
    writer.writerow(Dimention)
    writer.writerow('')
    writer.writerow(header2)
    writer.writerow(header)
    dataForm = []
    for i in data['DesignRules']:
        dataForm.append(i['Layers'])     
        dataForm.append(i['PadToPad'])
        dataForm.append(i['PadToTrack'])
        dataForm.append(i['TrackToTrack'])
        if 'MinLineWidth' in i:
        	dataForm.append(i['MinLineWidth'])
        else:
        	dataForm.append('-')
        if 'TrackToRegion' in i:
            dataForm.append(i['TrackToRegion'])
        else:
            dataForm.append('-')

        writer.writerow(dataForm)
        dataForm.clear()
    writer.writerow('')
    writer.writerow(header3)
    writer.writerow(MaterialStackup)
    for i in data['MaterialStackup']:
    	dataForm.append(i['Type'])
    	dataForm.append(i['Name'])
    	if 'Thickness' in i:
    		dataForm.append(i['Thickness'])
    	else:
    		dataForm.append('-')
    	if 'Material' in i:
    		dataForm.append(i['Material'])
    	else:
    		dataForm.append('-')
    	if 'Color' in i:
    		dataForm.append(i['Color'])
    	else:
    		dataForm.append('-')
    	if 'DielectricConstant' in i:
    		dataForm.append(i['DielectricConstant'])
    	else:
    		dataForm.append('-')

    	writer.writerow(dataForm)
    	dataForm.clear()

# Closing file
fj.close()
