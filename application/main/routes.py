
from flask import render_template, request,Blueprint
from application.models import Post

main = Blueprint("main",__name__)

@main.route("/")
@main.route("/home")
def home():
    page_no = request.args.get("page",1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3,page=page_no)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")