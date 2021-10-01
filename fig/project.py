from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
import json

# from flaskr.auth import login_required
# from flaskr.db import get_db

class UTGCollector(dict):

    def __init__(self):
        super(UTGCollector, self).__init__()
        self.idx = 0
        # print(self.idx)
        return
        

    def insert(self, classname, obj):
        if classname not in self.keys():
            self[classname] = {}
        self.idx += 1
        self[classname][self.idx] = obj
        print("\t%s.insert(%s, %s)"%(self.__class__.__name__,classname, repr(obj)))

        return self.idx
        
    def get(self, classname, idx=None):
        print("request get(%s, %s)"%(classname, str(idx)))
        if idx is None:
            if classname in list(self.keys()):
                return self[classname]
        else:
            if classname in self.keys():
                if idx in list(self[classname].keys()):
                    return self[classname][idx]
        return None

collector = UTGCollector()

class ProjectCl:

    def __init__(self, name, description):
        print("\t%s.__init__(%s,%s)"%(self.__class__.__name__, name, description))
        self.name = name
        self.description = description
        self.modules=[]
        self.id = collector.insert(self.__class__.__name__, self)
        
    def attach(self, module):
        self.modules.append(module)
        
        
    def delete(self):
        for m in self.modules:
            m.delete()
            del m
        self.modules=[]

    # def toJSON(self):
        # return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ProjectEncoder(json.JSONEncoder):

    def default(self, o):
        return o.__dict__


bp = Blueprint("project", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    # db = get_db()
    posts=()
    print("project index")
    data = collector.get("ProjectCl")
    print("data = ", repr(data))
    if data != None:
        posts=[]
        for k,v in data.items():
            # print(v.toJSON())
            JSONData = json.dumps(v, indent=4, cls=ProjectEncoder)
            print(JSONData)
            posts.append( {'id' : v.id, 'name': v.name, 'description' : v.description} )

    # posts = db.execute(
        # "SELECT p.id, title, body, created, author_id, username"
        # " FROM post p JOIN user u ON p.author_id = u.id"
        # " ORDER BY created DESC"
    # ).fetchall()
    return render_template("project/index.html", posts=posts)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        # get_db()
        # .execute(
            # "SELECT p.id, title, body, created, author_id, username"
            # " FROM post p JOIN user u ON p.author_id = u.id"
            # " WHERE p.id = ?",
            # (id,),
        # )
        # .fetchone()
    )

    # if post is None:
        # abort(404, f"Post id {id} doesn't exist.")

    # if check_author and post["author_id"] != g.user["id"]:
        # abort(403)

    return post


@bp.route("/project/create", methods=("GET", "POST"))
# @login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            ProjectCl(name, description)
            # db = get_db()
            # db.execute(
                # "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                # (title, body, g.user["id"]),
            # )
            # db.commit()
            return redirect(url_for("project.index"))

    return render_template("project/create.html")


@bp.route("/project/<int:id>/update", methods=("GET", "POST"))
# @login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        error = None

        if not name:
            error = "Name is required."

        if error is not None:
            flash(error)
        else:
            # db = get_db()
            # db.execute(
                # "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            # )
            # db.commit()
            return redirect(url_for("project.index"))

    return render_template("project/update.html", post=post)


@bp.route("/project/<int:id>/delete", methods=("POST",))
# @login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    # get_post(id)
    # db = get_db()
    # db.execute("DELETE FROM post WHERE id = ?", (id,))
    # db.commit()
    return redirect(url_for("project.index"))
