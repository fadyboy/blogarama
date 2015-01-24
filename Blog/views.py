# logic for page views
import mistune
from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_user, login_required
from werkzeug.security import check_password_hash

from Blog import app
from models import Post, User
from database import session

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # add functionality for pagination starting from zero indexed page
    page_index = page - 1
    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages -1
    has_previous = page_index > 0

    posts = session.query(Post).order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html", posts=posts, page=page, has_next=has_next, has_previous=has_previous,
                           total_pages=total_pages)

@app.route("/post/add", methods=['GET'])
@login_required
def add_post_get():

    return render_template('add_post.html')

@app.route("/post/add", methods=['POST'])
@login_required
def add_post_post():
    post = Post(
        title = request.form['title'],
        content = mistune.markdown(request.form['content'])
    )
    session.add(post)
    session.commit()

    return redirect(url_for("posts"))

# view individual post
@app.route("/post/<int:id>")
def view_post(id):
    # get post.id from posts page and query post based on number
    page_id =id
    post = session.query(Post).filter(Post.id == page_id).all()

    return render_template("view_post.html", post=post, page_id=page_id)

# edit selected post
@app.route("/post/<int:id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    # get post id for content and title to be pre-populated in form
    page_id = id
    post_details = session.query(Post).filter(Post.id == page_id)

    return render_template("edit_post.html", post_details=post_details)

@app.route("/post/<int:id>/edit", methods=["POST"])
@login_required
def edit_post_post(id):
    page_id = id

    post = session.query(Post).get(page_id)
    post.title = request.form['title']
    post.content = request.form['content']
    session.add(post)
    session.commit()

    # return to posts page after updating post

    return redirect(url_for("posts"))

# Select post for delete
@app.route("/post/<int:id>/delete")
@login_required
def delete_post(id):
    page_id = id

    # get the post based on the post id
    post = session.query(Post).get(page_id)

    return render_template("delete_post.html", post=post)

# confirm post to delete
@app.route("/<int:id>")
@login_required
def delete_post_confirm(id):
    page_id = id

    post = session.query(Post).get(page_id)
    session.delete(post)
    session.commit()

    return redirect(url_for("posts"))

# login page views
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    # pass in values from the submitted form
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()

    # check if user email and password match
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)

    return redirect(request.args.get('next') or url_for('posts'))







