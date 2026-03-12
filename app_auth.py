from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import hashlib, os, secrets, jwt

app = Flask(__name__)
CORS(app)

# Database: PostgreSQL on Vercel (via DATABASE_URL), SQLite locally
database_url = os.environ.get('DATABASE_URL', 'sqlite:///homeaway_auth.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'homeaway-dev-secret-change-in-production')

# AI Chat — GROQ_API_KEY must be set as env var
_groq_key = os.environ.get('GROQ_API_KEY')
from groq import Groq
client = Groq(api_key=_groq_key) if _groq_key else None

db = SQLAlchemy(app)

# ── MODELS ──

class User(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin      = db.Column(db.Boolean, default=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    host          = db.relationship('Host', backref='user', uselist=False)

    def set_password(self, password):
        salt = secrets.token_hex(16)
        self.password_hash = salt + ':' + hashlib.sha256((salt + password).encode()).hexdigest()

    def check_password(self, password):
        salt, hashed = self.password_hash.split(':', 1)
        return hashed == hashlib.sha256((salt + password).encode()).hexdigest()

    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'is_admin': self.is_admin, 'has_profile': self.host is not None}


class Traveller(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name    = db.Column(db.String(100), nullable=False)
    last_name     = db.Column(db.String(100), nullable=False)
    nationality   = db.Column(db.String(100))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    reviews       = db.relationship('Review', backref='traveller', lazy=True)

    def set_password(self, password):
        salt = secrets.token_hex(16)
        self.password_hash = salt + ':' + hashlib.sha256((salt + password).encode()).hexdigest()

    def check_password(self, password):
        salt, hashed = self.password_hash.split(':', 1)
        return hashed == hashlib.sha256((salt + password).encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id, 'email': self.email,
            'first_name': self.first_name, 'last_name': self.last_name,
            'full_name': f'{self.first_name} {self.last_name}',
            'nationality': self.nationality,
        }


class Host(db.Model):
    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    first_name       = db.Column(db.String(100), nullable=False)
    last_name        = db.Column(db.String(100), nullable=False)
    phone            = db.Column(db.String(30))
    bio              = db.Column(db.Text)
    nationality      = db.Column(db.String(100), nullable=False)
    nationality_code = db.Column(db.String(10), nullable=False)
    languages        = db.Column(db.String(300))
    address          = db.Column(db.String(300), nullable=False)
    city             = db.Column(db.String(100), nullable=False)
    country          = db.Column(db.String(100), nullable=False)
    lat              = db.Column(db.Float)
    lng              = db.Column(db.Float)
    hosting_since    = db.Column(db.String(20))
    max_guests       = db.Column(db.Integer, default=1)
    available        = db.Column(db.Boolean, default=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviews          = db.relationship('Review', backref='host', lazy=True, cascade='all, delete-orphan')

    def avg_rating(self):
        if not self.reviews: return None
        return round(sum(r.stars for r in self.reviews) / len(self.reviews), 1)

    def to_dict(self):
        avg = self.avg_rating()
        return {
            'id': self.id, 'user_id': self.user_id,
            'email': self.user.email if self.user else None,
            'first_name': self.first_name, 'last_name': self.last_name,
            'full_name': f'{self.first_name} {self.last_name}',
            'phone': self.phone, 'bio': self.bio,
            'nationality': self.nationality, 'nationality_code': self.nationality_code,
            'languages': self.languages.split(',') if self.languages else [],
            'address': self.address, 'city': self.city, 'country': self.country,
            'lat': self.lat, 'lng': self.lng,
            'maps_url': f"https://www.google.com/maps/search/?api=1&query={self.address.replace(' ', '+')}+{self.city.replace(' ', '+')}",
            'hosting_since': self.hosting_since, 'max_guests': self.max_guests, 'available': self.available,
            'avg_rating': avg, 'review_count': len(self.reviews),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class Review(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    host_id       = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    traveller_id  = db.Column(db.Integer, db.ForeignKey('traveller.id'), nullable=False)
    stars         = db.Column(db.Integer, nullable=False)
    cleanliness   = db.Column(db.Integer)
    hospitality   = db.Column(db.Integer)
    communication = db.Column(db.Integer)
    body          = db.Column(db.Text)
    photo_base64  = db.Column(db.Text)
    photo_mime    = db.Column(db.String(30))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        t = self.traveller
        return {
            'id': self.id, 'host_id': self.host_id, 'traveller_id': self.traveller_id,
            'traveller_name': t.full_name if t else 'Unknown',
            'traveller_nat': t.nationality if t else '',
            'stars': self.stars,
            'cleanliness': self.cleanliness, 'hospitality': self.hospitality, 'communication': self.communication,
            'body': self.body,
            'has_photo': self.photo_base64 is not None,
            'photo': f'data:{self.photo_mime};base64,{self.photo_base64}' if self.photo_base64 else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


# ── AUTH HELPERS ──

def make_token(user_id, role='host'):
    payload = {'user_id': user_id, 'role': role, 'exp': datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token: return jsonify({'error': 'No token provided'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if not user: return jsonify({'error': 'User not found'}), 401
            request.current_user = user
        except jwt.ExpiredSignatureError: return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError: return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

def require_traveller(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token: return jsonify({'error': 'No token provided'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if payload.get('role') != 'traveller':
                return jsonify({'error': 'Traveller account required'}), 403
            t = Traveller.query.get(payload['user_id'])
            if not t: return jsonify({'error': 'Traveller not found'}), 401
            request.current_traveller = t
        except jwt.ExpiredSignatureError: return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError: return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token: return jsonify({'error': 'No token provided'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if not user or not user.is_admin: return jsonify({'error': 'Admin access required'}), 403
            request.current_user = user
        except jwt.InvalidTokenError: return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated


# ── HOST AUTH ──

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email, password = data.get('email','').strip().lower(), data.get('password','')
    if not email or not password: return jsonify({'error': 'Email and password required'}), 400
    if len(password) < 6: return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if User.query.filter_by(email=email).first(): return jsonify({'error': 'Email already registered'}), 409
    user = User(email=email)
    user.set_password(password)
    db.session.add(user); db.session.commit()
    return jsonify({'token': make_token(user.id, 'host'), 'user': user.to_dict()}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email','').strip().lower()).first()
    if not user or not user.check_password(data.get('password','')): return jsonify({'error': 'Invalid email or password'}), 401
    return jsonify({'token': make_token(user.id, 'host'), 'user': user.to_dict()})

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def me():
    return jsonify(request.current_user.to_dict())


# ── TRAVELLER AUTH ──

@app.route('/api/traveller/register', methods=['POST'])
def traveller_register():
    data = request.get_json()
    email = data.get('email','').strip().lower()
    password = data.get('password','')
    first_name = data.get('first_name','').strip()
    last_name  = data.get('last_name','').strip()
    if not all([email, password, first_name, last_name]):
        return jsonify({'error': 'Email, password, first and last name required'}), 400
    if len(password) < 6: return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if Traveller.query.filter_by(email=email).first(): return jsonify({'error': 'Email already registered'}), 409
    t = Traveller(email=email, first_name=first_name, last_name=last_name, nationality=data.get('nationality',''))
    t.set_password(password)
    db.session.add(t); db.session.commit()
    return jsonify({'token': make_token(t.id, 'traveller'), 'traveller': t.to_dict()}), 201

@app.route('/api/traveller/login', methods=['POST'])
def traveller_login():
    data = request.get_json()
    t = Traveller.query.filter_by(email=data.get('email','').strip().lower()).first()
    if not t or not t.check_password(data.get('password','')): return jsonify({'error': 'Invalid email or password'}), 401
    return jsonify({'token': make_token(t.id, 'traveller'), 'traveller': t.to_dict()})

@app.route('/api/traveller/me', methods=['GET'])
@require_traveller
def traveller_me():
    return jsonify(request.current_traveller.to_dict())


# ── HOST PROFILE ──

@app.route('/api/profile', methods=['POST'])
@require_auth
def create_profile():
    u = request.current_user
    if u.host: return jsonify({'error': 'Profile already exists. Use PUT to update.'}), 409
    data = request.get_json()
    required = ['first_name','last_name','nationality','nationality_code','address','city','country']
    missing = [f for f in required if not data.get(f)]
    if missing: return jsonify({'error': f'Missing: {", ".join(missing)}'}), 400
    host = Host(
        user_id=u.id, first_name=data['first_name'], last_name=data['last_name'],
        phone=data.get('phone'), bio=data.get('bio'),
        nationality=data['nationality'], nationality_code=data['nationality_code'],
        languages=','.join(data.get('languages',[])) if isinstance(data.get('languages'),list) else data.get('languages',''),
        address=data['address'], city=data['city'], country=data['country'],
        lat=data.get('lat'), lng=data.get('lng'),
        hosting_since=data.get('hosting_since'), max_guests=data.get('max_guests',1), available=data.get('available',True),
    )
    db.session.add(host); db.session.commit()
    return jsonify(host.to_dict()), 201

@app.route('/api/profile', methods=['PUT'])
@require_auth
def update_profile():
    u = request.current_user
    if not u.host: return jsonify({'error': 'No profile found'}), 404
    data = request.get_json()
    host = u.host
    for field in ['first_name','last_name','phone','bio','nationality','nationality_code',
                  'address','city','country','lat','lng','hosting_since','max_guests','available']:
        if field in data: setattr(host, field, data[field])
    if 'languages' in data:
        host.languages = ','.join(data['languages']) if isinstance(data['languages'],list) else data['languages']
    host.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(host.to_dict())

@app.route('/api/profile', methods=['DELETE'])
@require_auth
def delete_profile():
    u = request.current_user
    if not u.host: return jsonify({'error': 'No profile found'}), 404
    db.session.delete(u.host); db.session.commit()
    return jsonify({'message': 'Profile deleted'})


# ── PUBLIC HOST LISTING ──

@app.route('/api/hosts', methods=['GET'])
def get_hosts():
    q = Host.query
    if nat := request.args.get('nationality'): q = q.filter_by(nationality_code=nat.upper())
    if city := request.args.get('city'): q = q.filter(Host.city.ilike(f'%{city}%'))
    if avail := request.args.get('available'): q = q.filter_by(available=(avail.lower()=='true'))
    hosts = q.order_by(Host.created_at.desc()).all()
    return jsonify({'hosts': [h.to_dict() for h in hosts], 'total': len(hosts)})

@app.route('/api/hosts/<int:host_id>', methods=['GET'])
def get_host(host_id):
    return jsonify(Host.query.get_or_404(host_id).to_dict())


# ── REVIEWS ──

@app.route('/api/hosts/<int:host_id>/reviews', methods=['GET'])
def get_reviews(host_id):
    Host.query.get_or_404(host_id)
    reviews = Review.query.filter_by(host_id=host_id).order_by(Review.created_at.desc()).all()
    avg = round(sum(r.stars for r in reviews) / len(reviews), 1) if reviews else None
    cat_avgs = {}
    if reviews:
        for cat in ['cleanliness','hospitality','communication']:
            vals = [getattr(r,cat) for r in reviews if getattr(r,cat) is not None]
            cat_avgs[cat] = round(sum(vals)/len(vals),1) if vals else None
    return jsonify({'reviews': [r.to_dict() for r in reviews], 'total': len(reviews), 'avg_rating': avg, 'category_avgs': cat_avgs})

@app.route('/api/hosts/<int:host_id>/reviews', methods=['POST'])
@require_traveller
def post_review(host_id):
    Host.query.get_or_404(host_id)
    t = request.current_traveller
    if Review.query.filter_by(host_id=host_id, traveller_id=t.id).first():
        return jsonify({'error': 'You have already reviewed this host'}), 409
    data = request.get_json()
    stars = data.get('stars')
    if not stars or not (1 <= int(stars) <= 5): return jsonify({'error': 'Stars must be 1–5'}), 400
    review = Review(
        host_id=host_id, traveller_id=t.id, stars=int(stars),
        cleanliness=int(data['cleanliness']) if data.get('cleanliness') else None,
        hospitality=int(data['hospitality']) if data.get('hospitality') else None,
        communication=int(data['communication']) if data.get('communication') else None,
        body=data.get('body','').strip() or None,
        photo_base64=data.get('photo_base64'), photo_mime=data.get('photo_mime','image/jpeg'),
    )
    db.session.add(review); db.session.commit()
    return jsonify(review.to_dict()), 201

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@require_traveller
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.traveller_id != request.current_traveller.id: return jsonify({'error': 'You can only delete your own reviews'}), 403
    db.session.delete(review); db.session.commit()
    return jsonify({'message': 'Review deleted'})


# ── ADMIN ──

@app.route('/api/admin/hosts/<int:host_id>', methods=['DELETE'])
@require_admin
def admin_delete_host(host_id):
    host = Host.query.get_or_404(host_id)
    db.session.delete(host); db.session.commit()
    return jsonify({'message': f'Host {host_id} deleted'})

@app.route('/api/admin/users', methods=['GET'])
@require_admin
def admin_list_users():
    return jsonify({'users': [u.to_dict() for u in User.query.all()]})

@app.route('/api/admin/reviews/<int:review_id>', methods=['DELETE'])
@require_admin
def admin_delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review); db.session.commit()
    return jsonify({'message': f'Review {review_id} deleted'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(is_admin=True).first():
            admin = User(email='admin@homeaway.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin); db.session.commit()
            print('✅ Admin created: admin@homeaway.com / admin123')
    app.run(debug=True, port=5000)