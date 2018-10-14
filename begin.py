from flask import Flask,render_template,url_for,flash,redirect

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html')

@app.route("/login",methods=['POST','GET'])
def login():
	return render_template('login.html',title='Login')

@app.route("/register",methods=['POST','GET'])
def register():   
		return render_template('register1.html',title='Register')

@app.route("/details",methods=['POST','GET'])
def details():
	return render_template('additional.html',title='Details')

if __name__ == '__main__':
	app.run(debug=True)



