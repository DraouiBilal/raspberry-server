from flask import Flask, request
import os

app = Flask(__name__)

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()
    return lines

def append_to_file(file_path, line):
    with open(file_path, 'a') as file:
        file.write(line + '\n')

def truncate_file(file_path):
    with open(file_path, 'r+') as file:
        file.truncate(0)

@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        users = read_from_file('users.txt')
        truncate_file("users.txt")
        return {"users": users}
    elif request.method == 'POST':
        # Append user to file
        user_data = request.get_json()
        if user_data and 'user' in user_data:
            user = user_data["user"]
            append_to_file('users.txt', user)
            return {"msg": f"User '{user}' appended to file."}
        else:
            return {"msg": "No user data received."}

@app.route('/score', methods=['GET', 'POST'])
def score():
    if request.method == 'GET':
        lines = read_from_file('score.txt')
        score = [{"user": line.split(" ")[0], "score": int(line.split(" ")[1])} for line in lines ]
        truncate_file("score.txt")
        return {"score": score}
    elif request.method == 'POST':
        # Append user to file
        score_data = request.get_json()
        if score_data and 'user' in score_data and 'score' in score_data:
            user = score_data["user"]
            score = score_data["score"]
            append_to_file('score.txt', f'{user} {score}')
            return {"msg": f"User '{user}' appended to file."}
        else:
            return {"msg": "No user or score data received."}


if __name__ == '__main__':
    app.run(port=5000)
