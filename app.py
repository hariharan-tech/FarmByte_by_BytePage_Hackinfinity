from flask import Flask , render_template , request
from flask_sqlalchemy import SQLAlchemy
import random , csv  ,sqlite3

app = Flask(__name__)
# file = open("products_shg.csv","r")
# reader = csv.DictReader(file,delimiter=",")
#d={}
#print(d)

try:
       conn = sqlite3.connect('users.db')
       conn.execute('''CREATE TABLE user_data 
              (name VARCHAR(40)  NOT NULL, 
              email           VARCHAR(40) PRIMARY KEY, 
              phone            VARCHAR(40)     NOT NULL, 
              pwd        VARCHAR(40)     NOT NULL, 
              addr       VARCHAR(40)     NOT NULL);''')
       conn.close()
except: 
       pass


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///products.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# app.config['SQLALCHEMY_BINDS']={
#     "users" : "sqlite:///users.db",
#     "sellers" : "sqlite:///sellers.db",
#     "cart" : "sqlite:///cart.db"
# }

db=SQLAlchemy(app)

#itemnog=2
# def generate_shoproducts():
#     #global itemnog
#     for i in reader:
#         items = Products(itemno=i['itemno'],title=i['title'],desc=i['desc'],price="Rs "+i['price'].split(" Rs")[0],creatorinfo=i['creator']+" from "+i['place'],review=round(random.uniform(66.67, 98.99), 2))
#     #items = Products(itemno=itemnog,title="Coir bags",desc="Coir bags straight from coconut trees",price="100",creatorinfo="ABC from chennai",review=round(random.uniform(66.67, 98.99), 2))
#         db.session.add(items)
#         db.session.commit()
# #     #itemnog+=1

class Products(db.Model):
    itemno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(200), nullable=False)
    creatorinfo = db.Column(db.String(200), nullable=False)
    review = db.Column(db.Float,nullable =False)

    def __repr__(self) -> str:
        return f"{self.itemno} - {self.title}"

# class Users(db.Model):
#     __bind_key__="users"
#     name = db.Column(db.String(200),primary_key=True)
#     email = db.Column(db.String(50),nullable=False)
#     phone = db.Column(db.String(20),nullable=False)
#     passw = db.Column(db.String(200),nullable=False)
#     addr = db.Column(db.String(200),nullable=False)
#     cart = db.relationship('Cart',backref='users')

#     def __repr__(self) -> str:
#         return f"{self.name} - {self.email}"

# class Sellers(db.Model):
#     __bind_key__="sellers"
#     name = db.Column(db.String(200),primary_key=True)
#     email = db.Column(db.String(50),nullable=False)
#     phone = db.Column(db.String(20),nullable=False)
#     addr = db.Column(db.String(200),nullable=False)

#     def __repr__(self) -> str:
#         return f"{self.name} - {self.email}"

# class Cart(db.Model):
#     __bind_key__="cart"
#     name = db.Column(db.String(200),primary_key=True)
#     itemno = db.Column(db.String(200),db.ForeignKey('user.name'),nullable=False)
#     status = db.Column(db.String(20),nullable=False)

#     def __repr__(self) -> str:
#         return f"{self.itemno} - {self.status}"

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/signupb",methods=['POST','GET'])
def signupb():
    if request.method=="POST":
        #print(request.form)
        frm = dict(request.form)
        #print(frm)
        try:
            conn = sqlite3.connect('users.db')
            conn.execute("INSERT INTO user_data VALUES('{}','{}','{}','{}','{}');".format(str(request.form['name']),str(frm['email']),str(frm['phone']),str(frm['password']),str(frm['address'])))
            conn.commit()
            conn.close()
            print("Success")
        except:
            print("Not success")
        return render_template("signupb.html",visibility="block")
    else:
        return render_template("signupb.html",visibility="none")


@app.route("/signups",methods=['POST','GET'])
def signups():
    if request.method=="POST":
        return render_template("signups.html",visibility="block")
    else:
        return render_template("signups.html",visibility="none")

@app.route("/shop")
def shop():
    #generate_shoproducts()
    allquery= Products.query.all()
    return render_template("shop.html",allquery=allquery) #,allquery=allquery

@app.route("/signinb",methods=['POST','GET'])
def signinb():
    if request.method=="POST":
        frm = dict(request.form)
        print(frm)
        try:
            conn = sqlite3.connect('users.db')
            data = conn.execute(f"select * from user_data where email='{frm['email']}' AND pwd='{frm['Password']}';")
            conn.commit()
            rows=[]
            #print(data)
            for row in data:
                rows.append(row)
            print(rows)
            if  len(rows)==1:
                print("Login Success")
                return render_template("user_profile.html", user=rows[0][0])
            else:
                print("Login Failed")
                return render_template("signinb.html",visibility="block")
            conn.close()
        except:
            print("Login Not success")
            return render_template("signinb.html",visibility="block")
    else:
        return render_template("signinb.html",visibility="none")
        pass

@app.route("/signins",methods=['POST','GET'])
def signins():
    if request.method=="POST":
        return render_template("signins.html",visibility="block")
    else:
        return render_template("signins.html",visibility="none")

@app.route("/contactus",methods=['POST','GET'])
def contactus():
    if request.method == "POST":
        print(request.form) #store them in data base (just run this to get the format of this list of tuples)
        return render_template("contact.html",visibility="block")
    else:
        return render_template("contact.html",visibility="none")

@app.route("/carts/<int:itemno>")
def cartsection(itemno):
    query= Products.query.get(itemno)
    return render_template("carts.html",query=query)

if __name__ == "__main__":
    app.run(debug=True)
