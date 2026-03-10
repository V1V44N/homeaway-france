"""
HomeAway France — Seed Script
Creates dummy hosts living across France.
Run app_auth.py first, then: python seed_france.py
"""

import requests

API = 'http://localhost:5000/api'

HOSTS = [
    # ── IMMIGRANTS / EXPATS IN FRANCE ──
    {
        'email': 'priya.sharma@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Priya', 'last_name': 'Sharma',
            'phone': '+33 6 11 22 33 44',
            'bio': 'Indian engineer in Paris for 5 years. Je cuisine du dal, du chai — I know every Indian grocery in the 10th arrondissement. Welcome home!',
            'nationality': 'Indian', 'nationality_code': 'IN',
            'languages': ['Hindi', 'English', 'French'],
            'address': '12 Rue du Faubourg Saint-Denis', 'city': 'Paris', 'country': 'France',
            'lat': 48.8697, 'lng': 2.3544,
            'hosting_since': '2021', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'wei.chen@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Wei', 'last_name': 'Chen',
            'phone': '+33 6 22 33 44 55',
            'bio': 'Born in Shanghai, settled in Paris 13th — the real Chinatown. I make homemade dumplings. Né à Shanghai, installé dans le vrai Chinatown parisien.',
            'nationality': 'Chinese', 'nationality_code': 'CN',
            'languages': ['Mandarin', 'Cantonese', 'French', 'English'],
            'address': '44 Avenue d\'Ivry', 'city': 'Paris', 'country': 'France',
            'lat': 48.8275, 'lng': 2.3585,
            'hosting_since': '2020', 'max_guests': 3, 'available': True,
        }
    },
    {
        'email': 'amara.diallo@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Amara', 'last_name': 'Diallo',
            'phone': '+33 6 33 44 55 66',
            'bio': 'Guinean heart, Lyonnais by adoption. Je prépare le yassa poulet comme ma mère. My home is always open — La maison est toujours ouverte.',
            'nationality': 'Nigerian', 'nationality_code': 'NG',
            'languages': ['French', 'Wolof', 'English'],
            'address': '18 Rue Moncey', 'city': 'Lyon', 'country': 'France',
            'lat': 45.7484, 'lng': 4.8320,
            'hosting_since': '2021', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'fatima.hassan@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Fatima', 'last_name': 'Al-Hassan',
            'phone': '+33 6 44 55 66 77',
            'bio': 'Egyptian in Marseille. I cook koshari and ful medames. Je vis dans le quartier du Belsunce — mon village loin de chez moi.',
            'nationality': 'Egyptian', 'nationality_code': 'EG',
            'languages': ['Arabic', 'French', 'English'],
            'address': '7 Rue des Chapeliers', 'city': 'Marseille', 'country': 'France',
            'lat': 43.2980, 'lng': 5.3738,
            'hosting_since': '2022', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'ali.demir@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Ali', 'last_name': 'Demir',
            'phone': '+33 6 55 66 77 88',
            'bio': 'Turkish architect in Strasbourg. Fresh simit every morning, çay all day. Grande communauté turque ici — you will feel right at home.',
            'nationality': 'Turkish', 'nationality_code': 'TR',
            'languages': ['Turkish', 'French', 'German', 'English'],
            'address': '23 Rue du Fossé des Tanneurs', 'city': 'Strasbourg', 'country': 'France',
            'lat': 48.5797, 'lng': 7.7448,
            'hosting_since': '2021', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'nguyen.thu@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Thu', 'last_name': 'Nguyen',
            'phone': '+33 6 66 77 88 99',
            'bio': 'Vietnamese, third generation in France. Je connais les meilleures soupes pho du 13ème. The best banh mi spots are no secret to me.',
            'nationality': 'Vietnamese', 'nationality_code': 'VN',
            'languages': ['Vietnamese', 'French', 'English'],
            'address': '108 Avenue de Choisy', 'city': 'Paris', 'country': 'France',
            'lat': 48.8189, 'lng': 2.3601,
            'hosting_since': '2020', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'kwame.asante@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Kwame', 'last_name': 'Asante',
            'phone': '+33 6 77 88 99 00',
            'bio': 'Ghanaian musician in Paris. Barbès is my village — je connais toute la communauté africaine. Jollof rice and waakye always on the stove.',
            'nationality': 'Ghanaian', 'nationality_code': 'GH',
            'languages': ['Twi', 'English', 'French'],
            'address': '18 Rue Dejean', 'city': 'Paris', 'country': 'France',
            'lat': 48.8872, 'lng': 2.3498,
            'hosting_since': '2022', 'max_guests': 1, 'available': True,
        }
    },
    {
        'email': 'sara.ahmed@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Sara', 'last_name': 'Ahmed',
            'phone': '+33 6 88 99 00 11',
            'bio': 'Pakistani doctor in Lille. Biryani every Friday — biryani tous les vendredis. Je connais les meilleures boucheries halal de la ville.',
            'nationality': 'Pakistani', 'nationality_code': 'PK',
            'languages': ['Urdu', 'Punjabi', 'French', 'English'],
            'address': '45 Rue Solférino', 'city': 'Lille', 'country': 'France',
            'lat': 50.6270, 'lng': 3.0554,
            'hosting_since': '2021', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'kenji.tanaka@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Kenji', 'last_name': 'Tanaka',
            'phone': '+33 6 99 00 11 22',
            'bio': 'Japanese developer in Bordeaux. I make authentic tonkotsu ramen from scratch. Je connais tous les spots japonais — you will not miss Tokyo.',
            'nationality': 'Japanese', 'nationality_code': 'JP',
            'languages': ['Japanese', 'French', 'English'],
            'address': '14 Rue Sainte-Catherine', 'city': 'Bordeaux', 'country': 'France',
            'lat': 44.8390, 'lng': -0.5730,
            'hosting_since': '2023', 'max_guests': 1, 'available': True,
        }
    },
    {
        'email': 'maria.santos@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Maria', 'last_name': 'Santos',
            'phone': '+33 6 00 11 22 33',
            'bio': 'Filipino nurse in Nice. I cook adobo and sinigang on weekends. La communauté philippine est très active sur la Côte d\'Azur — join us!',
            'nationality': 'Filipino', 'nationality_code': 'PH',
            'languages': ['Filipino', 'French', 'English'],
            'address': '5 Rue de la Préfecture', 'city': 'Nice', 'country': 'France',
            'lat': 43.6966, 'lng': 7.2742,
            'hosting_since': '2022', 'max_guests': 2, 'available': True,
        }
    },

    # ── FRENCH LOCALS WHO WELCOME SPECIFIC NATIONALITIES ──
    {
        'email': 'jean.dupont@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Jean', 'last_name': 'Dupont',
            'phone': '+33 6 12 00 34 56',
            'bio': 'Parisian who lived in Mumbai for 2 years. J\'adore accueillir des voyageurs indiens. I speak a little Hindi and love Indian culture.',
            'nationality': 'French', 'nationality_code': 'FR',
            'languages': ['French', 'English', 'Hindi (basic)'],
            'address': '3 Rue des Rosiers', 'city': 'Paris', 'country': 'France',
            'lat': 48.8553, 'lng': 2.3537,
            'hosting_since': '2022', 'max_guests': 2, 'available': True,
        }
    },
    {
        'email': 'claire.martin@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Claire', 'last_name': 'Martin',
            'phone': '+33 6 23 00 45 67',
            'bio': 'French teacher in Lyon, fluent in Mandarin. J\'adore la culture chinoise et j\'accueille les étudiants étrangers. I speak Chinese — 我说中文.',
            'nationality': 'French', 'nationality_code': 'FR',
            'languages': ['French', 'Mandarin', 'English'],
            'address': '7 Place Bellecour', 'city': 'Lyon', 'country': 'France',
            'lat': 45.7578, 'lng': 4.8320,
            'hosting_since': '2020', 'max_guests': 3, 'available': True,
        }
    },
    {
        'email': 'pierre.bernard@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Pierre', 'last_name': 'Bernard',
            'phone': '+33 6 34 00 56 78',
            'bio': 'Marseillais welcoming travellers from North Africa and the Middle East. Je parle arabe dialectal. My home is open to all — بيتي بيتك.',
            'nationality': 'French', 'nationality_code': 'FR',
            'languages': ['French', 'Arabic', 'English'],
            'address': '12 Cours Julien', 'city': 'Marseille', 'country': 'France',
            'lat': 43.2907, 'lng': 5.3844,
            'hosting_since': '2021', 'max_guests': 2, 'available': False,
        }
    },
    {
        'email': 'sophie.leroy@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Sophie', 'last_name': 'Leroy',
            'phone': '+33 6 45 00 67 89',
            'bio': 'Toulousaine, lived in Japan for 3 years. Je parle japonais couramment — I welcome Japanese and Korean travellers. Tokyo feels like my second home.',
            'nationality': 'French', 'nationality_code': 'FR',
            'languages': ['French', 'Japanese', 'English'],
            'address': '20 Rue Saint-Rome', 'city': 'Toulouse', 'country': 'France',
            'lat': 43.6047, 'lng': 1.4442,
            'hosting_since': '2023', 'max_guests': 1, 'available': True,
        }
    },
    {
        'email': 'lucas.petit@example.com',
        'password': 'password123',
        'profile': {
            'first_name': 'Lucas', 'last_name': 'Petit',
            'phone': '+33 6 56 00 78 90',
            'bio': 'Nantais passionate about Latin America. Je parle espagnol et portugais. Brazilian, Mexican, Argentine travellers — mi casa es su casa, ma maison est la vôtre.',            'nationality': 'French', 'nationality_code': 'FR',
            'languages': ['French', 'Spanish', 'Portuguese', 'English'],
            'address': '5 Place du Commerce', 'city': 'Nantes', 'country': 'France',
            'lat': 47.2129, 'lng': -1.5603,
            'hosting_since': '2022', 'max_guests': 2, 'available': True,
        }
    },
]

def seed():
    print(f'🌱 Seeding {len(HOSTS)} hosts across France...\n')
    success, skipped, failed = 0, 0, 0

    for h in HOSTS:
        email = h['email']

        res = requests.post(f'{API}/auth/register', json={
            'email': email, 'password': h['password']
        })

        if res.status_code == 409:
            print(f'⏭  {email} already exists — skipping')
            skipped += 1
            continue
        elif res.status_code != 201:
            print(f'❌  {email} register failed: {res.json().get("error")}')
            failed += 1
            continue

        token = res.json()['token']

        res2 = requests.post(f'{API}/profile',
            json=h['profile'],
            headers={'Authorization': f'Bearer {token}'}
        )

        if res2.status_code == 201:
            p = res2.json()
            print(f'✅  {p["full_name"]} ({p["nationality"]}) — {p["city"]}')
            success += 1
        else:
            print(f'❌  Profile failed for {email}: {res2.json().get("error")}')
            failed += 1

    print(f'\n─────────────────────────────────────────')
    print(f'✅ Created : {success}')
    print(f'⏭  Skipped : {skipped}')
    print(f'❌ Failed  : {failed}')
    print(f'\nAll passwords: password123')
    print(f'Admin: admin@homeaway.com / admin123')

if __name__ == '__main__':
    try:
        requests.get(f'{API}/hosts', timeout=3)
    except requests.ConnectionError:
        print('❌ Cannot reach backend. Make sure app_auth.py is running on port 5000.')
        exit(1)
    seed()
