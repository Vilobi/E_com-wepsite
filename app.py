from flask import Flask, render_template, redirect, url_for, session, request,jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "Vilobin"

app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'Vilobin@5758'
app.config["MYSQL_CURSORCLASS"] = 'DictCursor'
app.config["MYSQL_DB"] = 'snep'

mysql = MySQL(app)

def isloggedin():
    return "name" in session

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get('username')
        password=request.form.get('password')
        cur=mysql.connection.cursor()
        cur.execute("SELECT *FROM signup WHERE name=%s AND password=%s",(name,password))
        data=cur.fetchall()
        cur.close()
         
        
        if data:
            session['name']=name
            return redirect(url_for('home'))
        else:
            return "Invalide deatils"      
        
    return render_template('login.html')
    
    
@app.route("/signup",methods=["GET","POST"])

def signup():
    if request.method=="POST":
        name=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        
        cur=mysql.connection.cursor()
        cur.execute("select *from signup where name=%s",(name,))
        data=cur.fetchall()
        cur.close()
        
        if data:
            return "username is alredy exit"
        else:
            name=request.form.get("username")
            email=request.form.get("email")
            password=request.form.get("password")
        
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO signup (name,email,password) VALUES (%s,%s,%s)", (name,email,password))
            mysql.connection.commit()
            cur.close()
        return redirect(url_for('home'))
    return render_template("signup.html")




@app.route("/home", methods=["GET", "POST"])
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM deal")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', data=data)

@app.route("/add/<string:id>", methods=["GET", "POST"])   
def add(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM deal WHERE id=%s", (id,))
    data = cur.fetchone()
    cur.close()  
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM add_to_cart WHERE id=%s", (id,))
    dataa = cur.fetchone()
    cur.close()  
    
    if request.method == "POST":
        code = request.form.get("code")
        price = request.form.get("price")
        quantity = int(request.form.get("quantity"))
        images = request.form.get('img')
        
        if dataa:
            return "Alredy cart"
       
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO add_to_cart (code, quantity, price, images,id) VALUES (%s, %s, %s, %s,%s)", (code, quantity, price, images,data['id']))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('cart'))
             
    return render_template('Add.html', data=data) 

@app.route("/cart", methods=["GET", "POST"])
def cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM add_to_cart")
    data = cur.fetchall()
    cur.close()

    for i in data:
        i['quantity'] = int(i['quantity'])
        i['price'] = int(i['price'])
        i['total'] = i['quantity'] * i['price']  
    
    final_total = sum(i['total'] for i in data)
    
    return render_template("cart.html", data=data, final_total=final_total)




if __name__ == "__main__":
    app.run(debug=True)
