from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

# Store real-time location
locations = {}

# Simple user database (in production, use a real database)
users = {
    'driver1': {
        'password': generate_password_hash('driver123'),
        'role': 'driver'
    },
    'user1': {
        'password': generate_password_hash('user123'),
        'role': 'user'
    },
    # Add more users like this:
    'user2': {
        'password': generate_password_hash('user123'),
        'role': 'user'
    },
    
    'driver2': {
        'password': generate_password_hash('driver123'),
        'role': 'driver'
    },
     'driver3': {
        'password': generate_password_hash('driver123'),
        'role': 'driver'
    }
}


@app.route('/')
def index():
    if 'user' in session:
        if session['role'] == 'driver':
            return redirect(url_for('driver_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return render_template('login_choice.html')

@app.route('/login/<role>', methods=['GET', 'POST'])
def login(role):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        if user and check_password_hash(user['password'], password) and user['role'] == role:
            session['user'] = username
            session['role'] = role
            if role == 'driver':
                return redirect(url_for('driver_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        
        return render_template('login.html', error='Invalid credentials', role=role)
    
    return render_template('login.html', role=role)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/driver')
def driver_dashboard():
    if 'user' not in session or session.get('role') != 'driver':
        return redirect(url_for('login', role='driver'))
    return render_template('driver.html')

@app.route('/user')
def user_dashboard():
    if 'user' not in session or session.get('role') != 'user':
        return redirect(url_for('login', role='user'))
    return render_template('user.html')

@app.route('/update-location', methods=['POST'])
def update_location():
    if 'user' not in session:
        return jsonify({'status': 'unauthorized'}), 401
        
    data = request.get_json()
    user_id = session['user']
    locations[user_id] = {
        'lat': data['lat'],
        'lng': data['lng'],
        'role': session['role']
    }
    return jsonify({'status': 'success'})

@app.route('/get-locations')
def get_locations():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)
