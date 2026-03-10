from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homeaway.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── MODEL ──
class Host(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    # Personal
    first_name    = db.Column(db.String(100), nullable=False)
    last_name     = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(200), unique=True, nullable=False)
    phone         = db.Column(db.String(30))
    bio           = db.Column(db.Text)
    # Nationality / culture
    nationality   = db.Column(db.String(100), nullable=False)
    nationality_code = db.Column(db.String(10), nullable=False)  # e.g. "IN"
    languages     = db.Column(db.String(300))   # comma-separated e.g. "Hindi,English"
    # Location
    address       = db.Column(db.String(300), nullable=False)
    city          = db.Column(db.String(100), nullable=False)
    country       = db.Column(db.String(100), nullable=False)
    lat           = db.Column(db.Float)
    lng           = db.Column(db.Float)
    # Host info
    hosting_since = db.Column(db.String(20))
    max_guests    = db.Column(db.Integer, default=1)
    available     = db.Column(db.Boolean, default=True)
    # Timestamps
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id':               self.id,
            'first_name':       self.first_name,
            'last_name':        self.last_name,
            'full_name':        f'{self.first_name} {self.last_name}',
            'email':            self.email,
            'phone':            self.phone,
            'bio':              self.bio,
            'nationality':      self.nationality,
            'nationality_code': self.nationality_code,
            'languages':        self.languages.split(',') if self.languages else [],
            'address':          self.address,
            'city':             self.city,
            'country':          self.country,
            'lat':              self.lat,
            'lng':              self.lng,
            'maps_url':         f"https://www.google.com/maps/search/?api=1&query={self.address.replace(' ', '+')}+{self.city.replace(' ', '+')}",
            'hosting_since':    self.hosting_since,
            'max_guests':       self.max_guests,
            'available':        self.available,
            'created_at':       self.created_at.isoformat() if self.created_at else None,
            'updated_at':       self.updated_at.isoformat() if self.updated_at else None,
        }

# ── CREATE ──
@app.route('/api/hosts', methods=['POST'])
def create_host():
    data = request.get_json()
    required = ['first_name', 'last_name', 'email', 'nationality', 'nationality_code', 'address', 'city', 'country']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f'Missing fields: {", ".join(missing)}'}), 400

    if Host.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409

    host = Host(
        first_name       = data['first_name'],
        last_name        = data['last_name'],
        email            = data['email'],
        phone            = data.get('phone'),
        bio              = data.get('bio'),
        nationality      = data['nationality'],
        nationality_code = data['nationality_code'],
        languages        = ','.join(data.get('languages', [])) if isinstance(data.get('languages'), list) else data.get('languages', ''),
        address          = data['address'],
        city             = data['city'],
        country          = data['country'],
        lat              = data.get('lat'),
        lng              = data.get('lng'),
        hosting_since    = data.get('hosting_since'),
        max_guests       = data.get('max_guests', 1),
        available        = data.get('available', True),
    )
    db.session.add(host)
    db.session.commit()
    return jsonify(host.to_dict()), 201

# ── READ ALL ──
@app.route('/api/hosts', methods=['GET'])
def get_hosts():
    nationality = request.args.get('nationality')   # filter by nationality_code
    city        = request.args.get('city')
    available   = request.args.get('available')

    q = Host.query
    if nationality:
        q = q.filter_by(nationality_code=nationality.upper())
    if city:
        q = q.filter(Host.city.ilike(f'%{city}%'))
    if available is not None:
        q = q.filter_by(available=(available.lower() == 'true'))

    hosts = q.order_by(Host.created_at.desc()).all()
    return jsonify({'hosts': [h.to_dict() for h in hosts], 'total': len(hosts)})

# ── READ ONE ──
@app.route('/api/hosts/<int:host_id>', methods=['GET'])
def get_host(host_id):
    host = Host.query.get_or_404(host_id)
    return jsonify(host.to_dict())

# ── UPDATE ──
@app.route('/api/hosts/<int:host_id>', methods=['PUT'])
def update_host(host_id):
    host = Host.query.get_or_404(host_id)
    data = request.get_json()

    updatable = ['first_name','last_name','phone','bio','nationality','nationality_code',
                 'address','city','country','lat','lng','hosting_since','max_guests','available']

    for field in updatable:
        if field in data:
            setattr(host, field, data[field])

    if 'languages' in data:
        host.languages = ','.join(data['languages']) if isinstance(data['languages'], list) else data['languages']

    host.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(host.to_dict())

# ── DELETE ──
@app.route('/api/hosts/<int:host_id>', methods=['DELETE'])
def delete_host(host_id):
    host = Host.query.get_or_404(host_id)
    db.session.delete(host)
    db.session.commit()
    return jsonify({'message': f'Host {host_id} deleted'})

# ── SEED SAMPLE DATA ──
@app.route('/api/seed', methods=['POST'])
def seed():
    if Host.query.count() > 0:
        return jsonify({'message': 'Already seeded'}), 200
    samples = [
        dict(first_name='Priya',   last_name='Sharma',  email='priya@example.com',  nationality='Indian',    nationality_code='IN', phone='+44 7700 900001', bio='I love hosting travellers from back home. Home-cooked dal and chai always available!', languages=['Hindi','English','Gujarati'], address='14 Brick Lane',      city='London',  country='UK',     lat=51.521, lng=-0.0717, max_guests=2, available=True),
        dict(first_name='Wei',     last_name='Chen',    email='wei@example.com',    nationality='Chinese',   nationality_code='CN', phone='+33 6 12 34 56 78', bio='Happy to show you the best authentic Chinese spots in Paris.', languages=['Mandarin','Cantonese','French'], address='15 Rue de Turbigo', city='Paris',   country='France', lat=48.8627, lng=2.3522,  max_guests=3, available=True),
        dict(first_name='Kenji',   last_name='Tanaka',  email='kenji@example.com',  nationality='Japanese',  nationality_code='JP', phone='+1 415 555 0101', bio='Software engineer by day, passionate home cook. I make real ramen.', languages=['Japanese','English'], address='1822 Post Street',  city='San Francisco', country='USA', lat=37.7849, lng=-122.4294, max_guests=1, available=False),
        dict(first_name='Amara',   last_name='Okafor',  email='amara@example.com',  nationality='Nigerian',  nationality_code='NG', phone='+1 212 555 0188', bio='Nigerian-born New Yorker. I cook jollof rice that will remind you of home.', languages=['English','Yoruba','Igbo'], address='245 W 116th St', city='New York', country='USA', lat=40.8026, lng=-73.9535, max_guests=2, available=True),
        dict(first_name='Fatima',  last_name='Al-Hassan', email='fatima@example.com', nationality='Egyptian', nationality_code='EG', phone='+49 30 12345678', bio='I bring a piece of Cairo to Berlin — koshari, ful medames, and warm hospitality.', languages=['Arabic','German','English'], address='Sonnenallee 73', city='Berlin', country='Germany', lat=52.4764, lng=13.4333, max_guests=2, available=True),
    ]
    for s in samples:
        if not Host.query.filter_by(email=s['email']).first():
            s['languages'] = ','.join(s['languages'])
            db.session.add(Host(**s))
    db.session.commit()
    return jsonify({'message': f'Seeded {len(samples)} hosts'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
