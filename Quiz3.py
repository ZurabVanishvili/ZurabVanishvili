import requests
import json
import sqlite3

conn = sqlite3.connect('covid19stats.sqlite')
cursor = conn.cursor()

url = f'https://api.covidtracking.com/v1/us/daily.json'
r = requests.get(url)
info = r.content
print(r.status_code)
print( r.headers)
print(info)



with open('corona.json' , 'w')as file :
    getInfo = json.loads(info)
    pushInfo = json.dump(getInfo,file ,  indent=4)

for each in getInfo:

    print(each['date'] ,  'მონაცემებით კორონავირუსის მონაცემები შემდეგია: \nდადებითი:' ,
        each['positive'] ,'\nუარყოფითი:' , each['negative'] , '\nგარდაცვლილი:' , each['death'])


# მოცემულ ცხრილში მოგვაქვს ინფორმაცია თუ რამდენი დადებითი და უარყოფითი კოვიდშემთხვევა იყო კონკრეტულ დღეს.
# ამასთან ერთად გვაქვს წვდომა გარდაცვალების შემთხვევების რაოდენობასთან.

cursor.execute('''
CREATE TABLE IF NOT EXISTS covid19
(
datetime int  ,
positive int,
negative int ,
death int 
);

''')
for eachone in getInfo:

 cursor.execute('INSERT INTO covid19(datetime , positive , negative , death) VALUES(?, ? ,? ,?)' , (eachone['date'] , eachone['positive'] ,  eachone['negative']  , eachone['death']) )
 conn.commit()
 conn.close()
