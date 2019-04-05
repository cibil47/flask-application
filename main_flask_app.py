from flask import Flask, render_template,url_for,flash,redirect
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "admnujsgj45ljljdfZxfM"

posts = [
        {"author": "Jason",
         "title": "Artificial Intelligence",
         "posted_date":"Today",
         "content":"Something about artificial inelligence"
         },
        {"author": "Brody",
         "title": "Machine learning",
         "posted_date":"Yesterday",
         "content":"Machine learning is a sub field of artificial intelligence"
         },
        {"author": "Blog Bot",
         "title": "Deep learning",
         "posted_date":"Day before yesterday",
         "content":"Deep learning is a sub field of machine learning. We can do some cool stuff with deep learning"
         },
        ]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",  posts = posts)


@app.route("/about")
def about():
    return render_template("about.html",title = "About")


@app.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account created for {} !".format(form.username.data), "success")
        return redirect(url_for("home"))
    return render_template("register.html",title = "Register",form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html",title = "Login",form=form)


if __name__ == "__main__":
    app.run(debug=True)
