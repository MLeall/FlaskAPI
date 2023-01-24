# ****************************** #
# College	: Trebas Institute 
# Professor	: Iyad Koteich
# Class		: Edward
# Day		: 2023-01-10
# ****************************** #

#Importing Libres
#basis 
import hashlib, random

## Flask ##
from flask import Flask, make_response, jsonify, request

## sqlite3 ##
import sqlite3
from sqlite3 import Error

# Connecting to Database
mydb = None
target = 'python_flask.db'

# Create an Instance
app = Flask(__name__)


#Creating Routes
@app.route('/users', methods=['POST'])
def set_user():
	user 		= request.json
	
	#key 
	str2hash 	= user['email']+str(random.randint(100000,999999))
	hashresult 	= hashlib.md5(str2hash.encode())
	hashresult	= hashresult.hexdigest()

	mydb 	= sqlite3.connect(target)
	sql 	= f"INSERT INTO users (name, email, key) VALUES ('{user['name']}','{user['email']}','{hashresult}')"
	mycur 	= mydb.cursor()
	mycur.execute(sql)
	mydb.commit()

	return make_response(jsonify(	erro = '0',
									msg = 'sucess',
									key = hashresult)
	)

@app.route('/stores', methods=['GET'])
def get_store():
	mydb 		= sqlite3.connect(target)
	sql 		= f"SELECT id, name FROM stores"
	mycur 		= mydb.cursor()
	mycur.execute(sql)
	fech_stores = mycur.fetchall()

	stores 		= list()
	for store in fech_stores:
		stores.append(
			{
				'id': store[0],
				'name': store[1],
			}
		)
	return make_response(jsonify(	erro = '0',
									msg = '',
									data = stores)
	)

@app.route('/stores', methods=['POST'])
def set_store():
	store 		= request.json
	
	key		= store['key']
	name    = store['name']

	#getting the user id
	mydb 	= sqlite3.connect(target)
	mycur 	= mydb.cursor()
	sql 	= f"SELECT id FROM users WHERE key='{key}' LIMIT 1"
	mycur.execute(sql)
	user 	= mycur.fetchone()
	user_id	= user[0]

	sql 	= f"INSERT INTO stores (name, userId) VALUES ('{name}','{user_id}')"
	mycur2 	= mydb.cursor()
	mycur2.execute(sql)
	mydb.commit()

	return make_response(jsonify(	erro = '0',
									msg = 'sucess')
	)

@app.route('/products', methods=['GET'])
def get_product():
	mydb 		= sqlite3.connect(target)
	sql 		= f"SELECT id, name, price, (SELECT name FROM stores WHERE id = p.storeId) FROM products p"
	mycur 		= mydb.cursor()
	mycur.execute(sql)
	fech_products = mycur.fetchall()

	products 		= list()
	for product in fech_products:
		products.append(
			{
				'id': product[0],
				'name': product[1],
				'price': product[2],
				'store': product[3]
			}
		)
	return make_response(jsonify(	erro = '0',
									msg = '',
									data = products)
	)

@app.route('/products', methods=['POST'])
def set_product():
	product 		= request.json
	
	storeId	= product['store']
	name    = product['name']
	price	= product['price']

	sql 	= f"INSERT INTO products (name, price, storeId) VALUES ('{name}','{price}','{storeId}')"
	mydb 	= sqlite3.connect(target)
	mycur 	= mydb.cursor()
	mycur.execute(sql)
	mydb.commit()

	return make_response(jsonify(	erro = '0',
									msg = 'sucess')
	)

@app.route('/test', methods=['GET'])
def get_test():
	return make_response(jsonify(	erro = '0',
									msg = 'Test with GET sucess')
	)

@app.route('/test', methods=['POST'])
def set_test():
	json = request
	return make_response(jsonify(	erro = '0',
									msg = 'Test with POST sucess')
	)

# Starting the server 

app.run()