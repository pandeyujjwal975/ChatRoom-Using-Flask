from flask import Flask, render_template_string, session
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

users = set()  # Set to keep track of connected users

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ujjwal's Chat room</title>
        <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #d3d3d3;
            }
            #header {
                background-color: #1c6dd0;
                color: white;
                padding: 10px;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                position: relative;
            }
            #login-button {
                position: absolute;
                top: 10px;
                left: 10px;
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 16px;
                transition: background-color 0.3s;
            }
            #login-button:hover {
                background-color: #45a049;
            }
            #chat-container {
                display: flex;
                justify-content: space-between;
                padding: 20px;
                height: calc(100vh - 60px);
                box-sizing: border-box;
            }
            #chat {
                background-color: white;
                flex: 1;
                margin-right: 20px;
                border-radius: 15px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                padding: 15px;
                overflow-y: auto;
                display: flex;
                flex-direction: column-reverse;
            }
            #chat p {
                background-color: #f1f1f1;
                padding: 10px;
                border-radius: 15px;
                margin-bottom: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            #message-form {
                position: absolute;
                bottom: 20px;
                left: 20px;
                right: 20px;
                display: flex;
                justify-content: space-between;
            }
            #message {
                flex: 1;
                padding: 10px;
                font-size: 16px;
                border: 2px solid #d3d3d3;
                border-radius: 20px;
                margin-right: 10px;
                box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.1);
            }
            #send-button {
                padding: 10px 20px;
                background-color: #1c6dd0;
                color: white;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-size: 16px;
            }
            #send-button:hover {
                background-color: #1457a6;
            }
            #connected-users {
                width: 200px;
                background-color: #ffea00;
                padding: 15px;
                border-radius: 15px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                position: relative;
            }
            #connected-users h3 {
                margin: 0;
                background-color: #1c6dd0;
                color: white;
                padding: 10px;
                border-radius: 10px;
                text-align: center;
            }
            #users-list {
                list-style-type: none;
                padding: 0;
                margin-top: 15px;
            }
            #users-list li {
                padding: 5px;
                border-bottom: 1px solid #ccc;
            }
        </style>
    </head>
    <body>
        <div id="header">
            Ujjwal's Chat room
            <button id="login-button" onclick="setUsername()">Log In</button>
        </div>
        <div id="chat-container">
            <div id="chat"></div>
            <div id="connected-users">
                <h3>Connected Users</h3>
                <ul id="users-list"></ul>
            </div>
        </div>
        <div id="message-form">
            <input id="message" type="text" placeholder="Type Your Message..." />
            <button id="send-button">Send</button>
        </div>
        <script>
            var socket = io.connect('http://' + document.domain + ':' + location.port);
            var isLoggedIn = false;

            function setUsername() {
                var username = prompt("Enter your username:");
                if (username.trim() !== '') {
                    socket.emit('set_username', username);
                    isLoggedIn = true;
                    document.getElementById('login-button').style.display = 'none';
                }
            }

            socket.on('response', function(data) {
                if (isLoggedIn) {
                    var chat = document.getElementById('chat');
                    var message = document.createElement('p');
                    message.textContent = data.username + ': ' + data.message;
                    chat.appendChild(message);
                }
            });

            socket.on('update_users', function(users) {
                var usersList = document.getElementById('users-list');
                usersList.innerHTML = '';
                users.forEach(function(user) {
                    var li = document.createElement('li');
                    li.textContent = "Name: " + user + " | Status: Active";
                    usersList.appendChild(li);
                });
            });

            document.getElementById('send-button').addEventListener('click', function() {
                if (!isLoggedIn) {
                    alert('Please log in to send messages');
                    return;
                }
                var message = document.getElementById('message').value;
                if (message.trim() !== '') {
                    socket.send({message: message});
                    document.getElementById('message').value = '';
                }
            });

            socket.on('connect', function() {
                console.log('Connected to the chat server.');
            });
        </script>
    </body>
    </html>
    ''')

@socketio.on('set_username')
def set_username(username):
    # Store the username in the session
    session['username'] = username
    users.add(username)
    emit('update_users', list(users), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username:
        users.discard(username)
        emit('update_users', list(users), broadcast=True)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anonymous')
    print('Received message from', username, ':', data)
    emit('response', {'username': username, 'message': data['message']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)