# ****************************** #
# College	: Trebas Institute 
# Professor	: Iyad Koteich
# Student	: Edward / Matheus Leal
# Day		: 02-10-2023
# ****************************** #

# Imports
import hashlib, random
from flask import Flask, make_response, jsonify, request, render_template, redirect, url_for
import sqlite3	

mydb = None
target = 'python_flask.db'

app = Flask(__name__)

# Routes
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/form/user', methods=['GET'])
def form_user():
	return render_template('form_user.html')

@app.route('/form/store', methods=['GET'])
def form_store():
	return render_template('form_store.html')

@app.route('/form/product', methods=['GET'])
def form_product():
	return render_template('form_product.html')

@app.route('/users', methods=['GET'])
def get_user():
	mydb = sqlite3.connect(target)
	sql = f"SELECT id, name, email FROM users"
	mycur = mydb.cursor()
	mycur.execute(sql)
	fech_users = mycur.fetchall()

	users = list()
	for user in fech_users:
		users.append(
			{
				'id': user[0],
				'name': user[1],
				'email': user[2]
			}
		)
	return (jsonify(users))

@app.route('/form/set_user', methods=['POST'])
def set_user():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']

		# Creating a key 
		str2hash = email + str(random.randint(100000, 999999))
		hashresult = hashlib.md5(str2hash.encode())
		hashresult = hashresult.hexdigest()

		mydb = sqlite3.connect(target)
		sql = f"INSERT INTO users (name, email, key) VALUES ('{name}','{email}','{hashresult}')"
		mycur = mydb.cursor()
		mycur.execute(sql)
		mydb.commit()

		return redirect(url_for('index'))

@app.route('/stores', methods=['GET'])
def get_store():
	mydb = sqlite3.connect(target)
	sql = f"SELECT id, userId, name FROM stores"
	mycur = mydb.cursor()
	mycur.execute(sql)
	fetch_stores = mycur.fetchall()

	stores = list()
	for store in fetch_stores:
		stores.append(
			{
				'store_id': store[0],
				'user_id': store[1],
				'name': store[2],
			}
		)
	return jsonify(stores)

@app.route('/form/set_store', methods=['POST'])
def set_store():
	if request.method == 'POST':
		store_name = request.form['store_name']
		name = request.form['name']
		email = request.form['email']

		# Getting user id through name and email
		mydb = sqlite3.connect(target)
		mycur = mydb.cursor()
		sql = f"SELECT id FROM users WHERE name='{name}' AND email='{email}'"
		mycur.execute(sql)
		user = mycur.fetchone()
		user_id	= user[0]

		sql = f"INSERT INTO stores (name, userId) VALUES ('{store_name}', '{user_id}')"
		mycur2 	= mydb.cursor()
		mycur2.execute(sql)
		mydb.commit()

		return redirect(url_for('index'))

@app.route('/products', methods=['GET'])
def get_product():
	mydb = sqlite3.connect(target)
	sql = f"SELECT id, name, price, storeId FROM products"
	mycur = mydb.cursor()
	mycur.execute(sql)
	fetch_products = mycur.fetchall()

	products = list()
	for product in fetch_products:
		products.append(
			{
				'id': product[0],
				'name': product[1],
				'price': product[2],
				'store_id': product[3]
			}
		)
	return jsonify(products)

@app.route('/form/set_product', methods=['POST'])
def set_product():
	if request.method == 'POST':

		store_name = request.form['store_name']
		product_name = request.form['product_name']
		price = request.form['price']

		mydb = sqlite3.connect(target)
		sql = f"SELECT stores.id AS storeID FROM stores INNER JOIN users ON stores.userId = users.id WHERE stores.name='{store_name}'"
		mycur = mydb.cursor()
		mycur.execute(sql)
		fetch_id = mycur.fetchone()

		sql = f"INSERT INTO products (name, price, storeId) VALUES ('{product_name}','{price}','{fetch_id}')"
		mycur2 = mydb.cursor()
		mycur2.execute(sql)
		mydb.commit()

		return redirect(url_for('index'))

# Starting the server
app.run(debug=True)
