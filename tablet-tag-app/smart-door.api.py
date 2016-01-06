from flask import Flask, request, Response, jsonify
#from flaskext.mysql import mysql

#mysql = MySQL()
app = Flask(__name__)


DB = "smartdoor-tagging"
HOST=""
USER =""
PASSWORD=""

#app.config['MYSQL_DATABASE_USER'] = USER
#app.config['MYSQL_DATABASE_PASSWORD'] = PASSWORD
#app.config['MYSQL_DATABASE_DB'] = DB
#app.config['MYSQL_DATABASE_HOST'] = HOST


#mysql.init_app(app)

#con = mysql_connect()
#cur = con.cursor()


'''
SUGGESTED TABLE SCHEMA OR MEBBE USE EXISTING SCHEMA

TABLE 1: [TIMESTAMP, DIRECTION, NAME, COUNT]
TABLE 2: [TIMESTAMPT, NAME_LIST]

'''


#================================================================================================#

def update_current_occupancy_list():
	'''
		Use the information in the TABLE 1 to update TABLE 2 information; call this function after every entry in the TABLE 1
	'''
	pass

#================================================================================================#

'''
	This method queries the table which holds the data about the list of names in the lab
'''
@app.route('/get_count_and_names', methods=['POST','GET'])
def get_user_count_and_names():
		if request.method == 'GET':
			

			info="4,uddhav,utsav,karanj,prasad"
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

			'''
				add the name to the database with the direction 'in': write some function which adds the name to the table
			'''
			

			update_current_occupancy_list()

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

			'''
				add the name to the database with the direction 'out': write some function which adds the name to the table
			'''
			
			update_current_occupancy_list()

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