from flask import Flask, jsonify, request
from validators import validate_age

app = Flask(__name__)

users = [
    {"id": 1, "name": "john", "age": 20},
    {"id": 2, "name": "jane", "age": 24},
    {"id": 3, "name": "jill", "age": 35}
]

# get all users
@app.route("/users", methods=["GET"])
def get_user():
    return jsonify(users)


# create new user
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "name and age are required"}), 400
    
    # Validate age
    is_valid, age_or_error = validate_age(data["age"])
    if not is_valid:
        return jsonify({"error": age_or_error}), 400

    new_id = max(user["id"] for user in users) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": data["name"],
        "age": age_or_error  # Use the validated age
    }
    users.append(new_user)
    return jsonify(new_user), 201


# update existing user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    
    for user in users:
        if user["id"] == user_id:
            # Update name if provided
            if "name" in data:
                user["name"] = data["name"]

            # Update age with validation if provided
            if "age" in data:
                is_valid, age_or_error = validate_age(data["age"])
                if not is_valid:
                    return jsonify({"error": age_or_error}), 400
                user["age"] = age_or_error

            return jsonify(user)

    return jsonify({"error": "User not found"}), 404


# delete user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    updated_users = [u for u in users if u["id"] != user_id]
    if len(updated_users) == len(users):
        return jsonify({"error": "User not found"}), 404

    users = updated_users
    return jsonify({"message": f"User with id {user_id} deleted"}), 200


# required to run directly via python
if __name__ == "__main__":
    app.run(debug=True)