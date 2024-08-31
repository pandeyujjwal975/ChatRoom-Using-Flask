
## Flask Chat Room Application

### Overview
This Flask chat room application uses Flask and Flask-SocketIO to create a real-time chat environment. Users can join the chat room, set their usernames, and send messages that are broadcast to all connected clients.

### Key Features
- **Real-Time Communication:** Utilizes WebSockets for live chat.
- **User Management:** Users can set their username and view a list of active users.
- **Front-End Design:** Simple and responsive chat interface.

### Running the Application

1. **Install Dependencies:**
   Make sure you have Flask and Flask-SocketIO installed:
   ```bash
   pip install flask flask-socketio
   ```

2. **Save the Code:**
   Save the application code in a file named `app.py`.

3. **Start the Server:**
   Run the application using:
   ```bash
   python app.py
   ```

4. **Access the Chat Room:**
   Open your browser and navigate to `http://127.0.0.1:5000`.

### Usage
- **Log In:** Click the "Log In" button to set your username.
- **Send Messages:** Type messages in the input field and click "Send" to broadcast them to other users.
- **View Active Users:** Check the right sidebar for a list of active users.

### Additional Enhancements
- **Security Improvement:** Set a strong, unique `SECRET_KEY` for session management.
- **Error Handling:** Add error handling to manage unexpected disconnects or empty messages.
- **Persistent Storage:** Integrate a database if you want to store messages or user data permanently.
