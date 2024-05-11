from flask import Flask, request, jsonify
from instaloader import Instaloader

app = Flask(__name__)
L = Instaloader()


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Instagram API",
        "status": 200,
        "success": True
    }), 200


@app.route('/followers', methods=['GET'])
def get_followers():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is required"}), 400

    try:
        profile = L.check_profile_id(username)
        followers_count = profile.followers
        return jsonify({
            "username": username,
            "followers": followers_count,
            "success": True,
            "status": 200,
            "message": "Followers count fetched successfully"
        }), 200
    except Exception as e:
        print("error: ", e)
        if "Redirected to login page" in str(e):
            return jsonify({
                "error": "Something went wrong :(",
                "status": 500,
                "success": False,
                "message": "Please check the username and try again"
            }), 500
        return jsonify({
            "error": "User not found",
            "status": 404,
            "success": False,
            "message": "User not found"
        }), 404


if __name__ == '__main__':
    app.run(debug=False)
