@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Correctly render the login page if it's a GET request

    data = request.get_json()  # Expecting JSON data from the frontend
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'msg': 'Invalid password'}), 401

    # generate JWT token
    token = create_access_token(identity={'user_id': user.id, 'role': user.role}, expires_delta=datetime.timedelta(hours=1))

    return jsonify({'token': token})

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    data = request.get_json()  # Expecting JSON data from frontend
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'patient')  # default role

    if not email or not password:
        return jsonify({'msg': 'Missing email or password'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 409

    # Hash password using bcrypt
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(name=name, email=email, password=hashed, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'User successfully registered'}), 201
