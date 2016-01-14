from flask import Flask, request, Response, jsonify
from flaskext.mysql import MySQL
from datetime import datetime

mysql = MySQL()
app = Flask(__name__)


DB = "labcount"
HOST="10.129.23.100"
USER ="lab_count_info"
PASSWORD="smart_count"

app.config['MYSQL_DATABASE_USER'] = USER
app.config['MYSQL_DATABASE_PASSWORD'] = PASSWORD
app.config['MYSQL_DATABASE_DB'] = DB
app.config['MYSQL_DATABASE_HOST'] = HOST


mysql.init_app(app)

con = mysql.connect()
cur = con.cursor()


'''
SUGGESTED TABLE SCHEMA OR MEBBE USE EXISTING SCHEMA

TABLE 1: [TIMESTAMP, DIRECTION, NAME, COUNT]
TABLE 2: [TIMESTAMPT, NAME_LIST]

'''


#================================================================================================#

def update_current_occupancy_list(count,name,dir):

	query = "select namelist from present_occupancy where id = (select max(id) from present_occupancy);"
	cur.execute(query)
	res = cur.fetchone()
	string = ""
	if res is not None:
		string = str(res[0])



    	if dir == "in":
		if string == "" or name not in string:
		    if string == "":
			    string += name
	            else:
			    string += "," + name
		    query = "insert into present_occupancy(ts,namelist) values('%s','%s')" %(datetime.now(),string)
		    cur.execute(query)
		    con.commit()
		    
		    count += 1
		    query = "insert into occupancy_activity(ts,direction,name, count) values('%s','%s','%s',%d)" %(datetime.now(),'in',name, count)
		    cur.execute(query)
		    con.commit()
		    print "presence_status updated"            
		    
	elif dir == "out":
		print string
		parts = string.split(",")
		if len(parts) != 0:
			if name in parts:
				if count != 0:  
		    			count -= 1   
				parts.remove(name)
				string = ",".join(parts)
				print string
		
				query = "insert into occupancy_activity(ts,direction,name, count) values('%s','%s','%s',%d)" %(datetime.now(),'out',name,count)
				cur.execute(query)
				con.commit()
				print "presence_status updated"

				query = "insert into present_occupancy(ts,namelist) values('%s','%s')" %(datetime.now(),string)
				cur.execute(query)
				con.commit()

	'''
		Use the information in the TABLE 1 to update TABLE 2 information; call this function after every entry in the TABLE 1
	'''

#================================================================================================#

'''
	This method queries the table which holds the data about the list of names in the lab
'''
@app.route('/get_count_and_names', methods=['POST','GET'])
def get_user_count_and_names():
		if request.method == 'GET':
            #info="4,uddhav,utsav,karanj,prasad"
			query = "select count from occupancy_activity where id = (select max(id) from occupancy_activity);"
			cur.execute(query)
			res = cur.fetchone()
			if res == None:
				count = 0
				print 'a'
			else:
				count = str(res[0])
				print 'b'
			print count
			
			query = "select namelist from present_occupancy where id = (select max(id) from present_occupancy);"
			cur.execute(query)
			res = cur.fetchone()
			print res
			if res == None or res[0] == '':
				namelist = "No Occupancy"
			else:
				namelist = str(res[0])
			
			info = str(count) + "," + namelist
			'''
				get the name list from the TABLE 2: write a function to get the current occupancy in the format occupancy_count,name1,name2,...nameN
			'''

			cb = request.args.get('callback')
			resp = "%s('%s')" %(cb, info)
			return Response(resp, mimetype='application/javascript')

		elif request.method == 'POST':
			return 'post request not supported'

#================================================================================================#
'''
	This method adds the tag with the 'IN' direction in the table TABLE 1
'''
@app.route('/in_entry', methods=['POST', 'GET'])
def add_in_user_entry():
		if request.method == 'GET':
			name = request.args.get('name')
			print name # tagged name is stored here
			count = 0	
			cur.execute("select count(*) from occupancy_activity;")
			res = cur.fetchone()
			if res[0] == 0:
				count = 0
			else :
				query = "select count from occupancy_activity where id = (select max(id) from occupancy_activity);"
				cur.execute(query)
				res = cur.fetchone()
				count = int(res[0])
				
			update_current_occupancy_list(count,name,"in")

			cb = request.args.get('callback')
			resp = "%s('%s')" %(cb, name)
			return Response(resp, mimetype='application/javascript')

		elif request.method == 'POST':
			return 'post request not supported'

#================================================================================================#
'''
	This method adds the tag with the 'OUT' direction in the table TABLE 1
'''
@app.route('/out_entry', methods=['POST', 'GET'])
def add_out_user_entry():
		if request.method == 'GET':

			name = request.args.get('name')
			print name #tagged name is stored here

			count = 0	
			cur.execute("select count(*) from occupancy_activity;")
			res = cur.fetchone()
			if res[0] == 0:
				count = 0
			else :
				query = "select count from occupancy_activity where id = (select max(id) from occupancy_activity);"
				cur.execute(query)
				res = cur.fetchone()
				count = int(res[0])

			'''
				add the name to the database with the direction 'out': write some function which adds the name to the table
			'''
			
			update_current_occupancy_list(count,name,"out")

			cb = request.args.get('callback')
			resp = "%s('%s')" %(cb, name)
			return Response(resp, mimetype='application/javascript')

		elif request.method == 'POST':
			return 'post request not supported'


#================================================================================================#

@app.route('/')
def index():
	return 'it works'


if __name__ == '__main__':
	app.run('0.0.0.0',port=7000, debug=True)
