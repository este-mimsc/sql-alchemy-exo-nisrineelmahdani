from flask import Flask, jsonify, request
from extensions import db, migrate
from models import User, Post


def create_app():
    app = Flask(__name__)

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Flask + SQLAlchemy assignment"})

    # ---------------------------
    # USERS
    # ---------------------------
    @app.route("/users", methods=["GET", "POST"])
    def users():
        if request.method == "POST":
            data = request.get_json()

            username = data.get("username")
            email = data.get("email")

            if not username or not email:
                return jsonify({"error": "username and email required"}), 400

            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()

            return jsonify({"message": "User created", "id": user.id}), 201

        # GET
        users = User.query.all()
        users_list = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
            for user in users
        ]

        return jsonify(users_list), 200

    # ---------------------------
    # POSTS
    # ---------------------------
    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        if request.method == "POST":
            data = request.get_json()

            title = data.get("title")
            content = data.get("content")
            user_id = data.get("user_id")

            if not title or not content or not user_id:
                return jsonify({"error": "title, content, user_id required"}), 400

            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

            post = Post(title=title, content=content, user_id=user_id)
            db.session.add(post)
            db.session.commit()

            return jsonify({
                "message": "Post created successfully",
                "id": post.id
            }), 201

        # GET
        posts = Post.query.all()
        posts_list = [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": {
                    "id": post.author.id,
                    "username": post.author.username,
                    "email": post.author.email,
                }
            }
            for post in posts
        ]

        return jsonify(posts_list), 200

    return app


# Only executed when running "python app.py"
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
