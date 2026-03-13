import requests
import random
import time

# Total countries: ~195 logic 
COUNTRIES = [
    ("Afghanistan", "AF", "Afghan", "Pashto,Dari,English"),
    ("Albania", "AL", "Albanian", "Albanian,English"),
    ("Algeria", "DZ", "Algerian", "Arabic,French,Berber"),
    ("Andorra", "AD", "Andorran", "Catalan,Spanish,French"),
    ("Angola", "AO", "Angolan", "Portuguese,Umbundu"),
    ("Antigua and Barbuda", "AG", "Antiguan, Barbudan", "English"),
    ("Argentina", "AR", "Argentine", "Spanish,English"),
    ("Armenia", "AM", "Armenian", "Armenian,Russian"),
    ("Australia", "AU", "Australian", "English"),
    ("Austria", "AT", "Austrian", "German,English"),
    ("Azerbaijan", "AZ", "Azerbaijani", "Azerbaijani,Russian"),
    ("Bahamas", "BS", "Bahamian", "English"),
    ("Bahrain", "BH", "Bahraini", "Arabic,English"),
    ("Bangladesh", "BD", "Bangladeshi", "Bengali,English"),
    ("Barbados", "BB", "Barbadian", "English"),
    ("Belarus", "BY", "Belarusian", "Belarusian,Russian"),
    ("Belgium", "BE", "Belgian", "Dutch,French,German"),
    ("Belize", "BZ", "Belizean", "English,Spanish"),
    ("Benin", "BJ", "Beninese", "French,Fon"),
    ("Bhutan", "BT", "Bhutanese", "Dzongkha,English"),
    ("Bolivia", "BO", "Bolivian", "Spanish,Quechua,Aymara"),
    ("Bosnia and Herzegovina", "BA", "Bosnian, Herzegovinian", "Bosnian,Croatian,Serbian"),
    ("Botswana", "BW", "Motswana", "English,Setswana"),
    ("Brazil", "BR", "Brazilian", "Portuguese,English"),
    ("Brunei", "BN", "Bruneian", "Malay,English"),
    ("Bulgaria", "BG", "Bulgarian", "Bulgarian,English"),
    ("Burkina Faso", "BF", "Burkinabe", "French,Moore"),
    ("Burundi", "BI", "Burundian", "Kirundi,French,English"),
    ("Cabo Verde", "CV", "Cabo Verdean", "Portuguese,Kabuverdianu"),
    ("Cambodia", "KH", "Cambodian", "Khmer,French,English"),
    ("Cameroon", "CM", "Cameroonian", "French,English"),
    ("Canada", "CA", "Canadian", "English,French"),
    ("Central African Republic", "CF", "Central African", "Sango,French"),
    ("Chad", "TD", "Chadian", "French,Arabic"),
    ("Chile", "CL", "Chilean", "Spanish,English"),
    ("China", "CN", "Chinese", "Mandarin,English"),
    ("Colombia", "CO", "Colombian", "Spanish,English"),
    ("Comoros", "KM", "Comoran", "Comorian,Arabic,French"),
    ("Congo (Congo-Brazzaville)", "CG", "Congolese", "French,Lingala"),
    ("Costa Rica", "CR", "Costa Rican", "Spanish,English"),
    ("Croatia", "HR", "Croatian", "Croatian,English"),
    ("Cuba", "CU", "Cuban", "Spanish"),
    ("Cyprus", "CY", "Cypriot", "Greek,Turkish,English"),
    ("Czechia", "CZ", "Czech", "Czech,English"),
    ("Democratic Republic of the Congo", "CD", "Congolese", "French,Lingala,Swahili"),
    ("Denmark", "DK", "Danish", "Danish,English"),
    ("Djibouti", "DJ", "Djiboutian", "French,Arabic"),
    ("Dominica", "DM", "Dominican", "English,French Patois"),
    ("Dominican Republic", "DO", "Dominican", "Spanish,English"),
    ("Ecuador", "EC", "Ecuadorian", "Spanish,Quechua"),
    ("Egypt", "EG", "Egyptian", "Arabic,English,French"),
    ("El Salvador", "SV", "Salvadoran", "Spanish,English"),
    ("Equatorial Guinea", "GQ", "Equatoguinean", "Spanish,French,Portuguese"),
    ("Eritrea", "ER", "Eritrean", "Tigrinya,Arabic,English"),
    ("Estonia", "EE", "Estonian", "Estonian,Russian,English"),
    ("Eswatini", "SZ", "Swazi", "Swazi,English"),
    ("Ethiopia", "ET", "Ethiopian", "Amharic,Oromo,English"),
    ("Fiji", "FJ", "Fijian", "English,Fijian,Hindi"),
    ("Finland", "FI", "Finnish", "Finnish,Swedish,English"),
    ("France", "FR", "French", "French,English"),
    ("Gabon", "GA", "Gabonese", "French,Fang"),
    ("Gambia", "GM", "Gambian", "English,Mandinka"),
    ("Georgia", "GE", "Georgian", "Georgian,Russian,English"),
    ("Germany", "DE", "German", "German,English"),
    ("Ghana", "GH", "Ghanaian", "English,Akan,Ewe"),
    ("Greece", "GR", "Greek", "Greek,English"),
    ("Grenada", "GD", "Grenadian", "English,French Patois"),
    ("Guatemala", "GT", "Guatemalan", "Spanish"),
    ("Guinea", "GN", "Guinean", "French,Pular,Maninka"),
    ("Guinea-Bissau", "GW", "Bissau-Guinean", "Portuguese,Crioulo"),
    ("Guyana", "GY", "Guyanese", "English,Guyanese Creole"),
    ("Haiti", "HT", "Haitian", "French,Haitian Creole"),
    ("Honduras", "HN", "Honduran", "Spanish"),
    ("Hungary", "HU", "Hungarian", "Hungarian,English"),
    ("Iceland", "IS", "Icelandic", "Icelandic,English"),
    ("India", "IN", "Indian", "Hindi,English,Tamil,Telugu"),
    ("Indonesia", "ID", "Indonesian", "Indonesian,Javanese,English"),
    ("Iran", "IR", "Iranian", "Persian"),
    ("Iraq", "IQ", "Iraqi", "Arabic,Kurdish"),
    ("Ireland", "IE", "Irish", "English,Irish"),
    ("Israel", "IL", "Israeli", "Hebrew,Arabic,English"),
    ("Italy", "IT", "Italian", "Italian,English"),
    ("Jamaica", "JM", "Jamaican", "English,Jamaican Patois"),
    ("Japan", "JP", "Japanese", "Japanese,English"),
    ("Jordan", "JO", "Jordanian", "Arabic,English"),
    ("Kazakhstan", "KZ", "Kazakhstani", "Kazakh,Russian"),
    ("Kenya", "KE", "Kenyan", "Swahili,English"),
    ("Kiribati", "KI", "I-Kiribati", "English,Gilbertese"),
    ("Kuwait", "KW", "Kuwaiti", "Arabic,English"),
    ("Kyrgyzstan", "KG", "Kyrgyzstani", "Kyrgyz,Russian"),
    ("Laos", "LA", "Lao", "Lao,French"),
    ("Latvia", "LV", "Latvian", "Latvian,Russian,English"),
    ("Lebanon", "LB", "Lebanese", "Arabic,French,English"),
    ("Lesotho", "LS", "Mosotho", "Sesotho,English"),
    ("Liberia", "LR", "Liberian", "English"),
    ("Libya", "LY", "Libyan", "Arabic,Italian,English"),
    ("Liechtenstein", "LI", "Liechtensteiner", "German"),
    ("Lithuania", "LT", "Lithuanian", "Lithuanian,Russian,English"),
    ("Luxembourg", "LU", "Luxembourger", "Luxembourgish,French,German"),
    ("Madagascar", "MG", "Malagasy", "Malagasy,French"),
    ("Malawi", "MW", "Malawian", "English,Chichewa"),
    ("Malaysia", "MY", "Malaysian", "Malay,English,Mandarin,Tamil"),
    ("Maldives", "MV", "Maldivian", "Dhivehi,English"),
    ("Mali", "ML", "Malian", "French,Bambara"),
    ("Malta", "MT", "Maltese", "Maltese,English"),
    ("Marshall Islands", "MH", "Marshallese", "Marshallese,English"),
    ("Mauritania", "MR", "Mauritanian", "Arabic,French"),
    ("Mauritius", "MU", "Mauritian", "English,French,Creole"),
    ("Mexico", "MX", "Mexican", "Spanish,English"),
    ("Micronesia", "FM", "Micronesian", "English"),
    ("Moldova", "MD", "Moldovan", "Romanian,Russian"),
    ("Monaco", "MC", "Monegasque", "French,Italian,English"),
    ("Mongolia", "MN", "Mongolian", "Mongolian,Russian"),
    ("Montenegro", "ME", "Montenegrin", "Montenegrin,Serbian"),
    ("Morocco", "MA", "Moroccan", "Arabic,Berber,French"),
    ("Mozambique", "MZ", "Mozambican", "Portuguese,Makhuwa"),
    ("Myanmar", "MM", "Burmese", "Burmese,English"),
    ("Namibia", "NA", "Namibian", "English,Afrikaans,German"),
    ("Nauru", "NR", "Nauruan", "Nauruan,English"),
    ("Nepal", "NP", "Nepali", "Nepali,English"),
    ("Netherlands", "NL", "Dutch", "Dutch,English"),
    ("New Zealand", "NZ", "New Zealander", "English,Maori"),
    ("Nicaragua", "NI", "Nicaraguan", "Spanish"),
    ("Niger", "NE", "Nigerien", "French,Hausa,Zarma"),
    ("Nigeria", "NG", "Nigerian", "English,Hausa,Yoruba,Igbo"),
    ("North Korea", "KP", "North Korean", "Korean"),
    ("North Macedonia", "MK", "Macedonian", "Macedonian,Albanian"),
    ("Norway", "NO", "Norwegian", "Norwegian,English"),
    ("Oman", "OM", "Omani", "Arabic,English"),
    ("Pakistan", "PK", "Pakistani", "Urdu,English,Punjabi,Pashto"),
    ("Palau", "PW", "Palauan", "Palauan,English"),
    ("Palestine State", "PS", "Palestinian", "Arabic,English"),
    ("Panama", "PA", "Panamanian", "Spanish,English"),
    ("Papua New Guinea", "PG", "Papua New Guinean", "English,Tok Pisin"),
    ("Paraguay", "PY", "Paraguayan", "Spanish,Guarani"),
    ("Peru", "PE", "Peruvian", "Spanish,Quechua,Aymara"),
    ("Philippines", "PH", "Filipino", "Filipino,English"),
    ("Poland", "PL", "Polish", "Polish,English"),
    ("Portugal", "PT", "Portuguese", "Portuguese,English"),
    ("Qatar", "QA", "Qatari", "Arabic,English"),
    ("Romania", "RO", "Romanian", "Romanian,English"),
    ("Russia", "RU", "Russian", "Russian,English"),
    ("Rwanda", "RW", "Rwandan", "Kinyarwanda,French,English"),
    ("Saint Kitts and Nevis", "KN", "Kittitian", "English"),
    ("Saint Lucia", "LC", "Saint Lucian", "English,French Patois"),
    ("Saint Vincent and the Grenadines", "VC", "Saint Vincentian", "English,Vincentian Creole"),
    ("Samoa", "WS", "Samoan", "Samoan,English"),
    ("San Marino", "SM", "Sammarinese", "Italian"),
    ("Sao Tome and Principe", "ST", "Sao Tomean", "Portuguese"),
    ("Saudi Arabia", "SA", "Saudi", "Arabic,English"),
    ("Senegal", "SN", "Senegalese", "French,Wolof"),
    ("Serbia", "RS", "Serbian", "Serbian,English"),
    ("Seychelles", "SC", "Seychellois", "English,French,Creole"),
    ("Sierra Leone", "SL", "Sierra Leonean", "English,Krio"),
    ("Singapore", "SG", "Singaporean", "English,Malay,Mandarin,Tamil"),
    ("Slovakia", "SK", "Slovak", "Slovak,English"),
    ("Slovenia", "SI", "Slovenian", "Slovenian,English"),
    ("Solomon Islands", "SB", "Solomon Islander", "English,Pijin"),
    ("Somalia", "SO", "Somali", "Somali,Arabic"),
    ("South Africa", "ZA", "South African", "Zulu,Xhosa,Afrikaans,English"),
    ("South Korea", "KR", "South Korean", "Korean,English"),
    ("South Sudan", "SS", "South Sudanese", "English,Arabic"),
    ("Spain", "ES", "Spanish", "Spanish,English"),
    ("Sri Lanka", "LK", "Sri Lankan", "Sinhala,Tamil,English"),
    ("Sudan", "SD", "Sudanese", "Arabic,English"),
    ("Suriname", "SR", "Surinamese", "Dutch,Sranan Tongo,English"),
    ("Sweden", "SE", "Swedish", "Swedish,English"),
    ("Switzerland", "CH", "Swiss", "German,French,Italian,English"),
    ("Syria", "SY", "Syrian", "Arabic"),
    ("Tajikistan", "TJ", "Tajikistani", "Tajik,Russian"),
    ("Tanzania", "TZ", "Tanzanian", "Swahili,English"),
    ("Thailand", "TH", "Thai", "Thai,English"),
    ("Timor-Leste", "TL", "Timorese", "Tetum,Portuguese,Indonesian,English"),
    ("Togo", "TG", "Togolese", "French,Ewe"),
    ("Tonga", "TO", "Tongan", "Tongan,English"),
    ("Trinidad and Tobago", "TT", "Trinidadian", "English"),
    ("Tunisia", "TN", "Tunisian", "Arabic,French"),
    ("Turkey", "TR", "Turkish", "Turkish,English"),
    ("Turkmenistan", "TM", "Turkmen", "Turkmen,Russian"),
    ("Tuvalu", "TV", "Tuvaluan", "Tuvaluan,English"),
    ("Uganda", "UG", "Ugandan", "English,Swahili,Luganda"),
    ("Ukraine", "UA", "Ukrainian", "Ukrainian,Russian,English"),
    ("United Arab Emirates", "AE", "Emirati", "Arabic,English"),
    ("United Kingdom", "GB", "British", "English"),
    ("United States of America", "US", "American", "English,Spanish"),
    ("Uruguay", "UY", "Uruguayan", "Spanish"),
    ("Uzbekistan", "UZ", "Uzbekistani", "Uzbek,Russian"),
    ("Vanuatu", "VU", "Ni-Vanuatu", "Bislama,English,French"),
    ("Venezuela", "VE", "Venezuelan", "Spanish"),
    ("Vietnam", "VN", "Vietnamese", "Vietnamese,English"),
    ("Yemen", "YE", "Yemeni", "Arabic"),
    ("Zambia", "ZM", "Zambian", "English,Bemba,Nyanja"),
    ("Zimbabwe", "ZW", "Zimbabwean", "English,Shona,Ndebele")
]

FIRST_NAMES = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mallory", "Nina", "Oscar", "Peggy", "Romeo", "Sybil", "Trent", "Victor", "Walter", "Zoe", "Ahmed", "Maria", "Wei", "Juan", "Yuki", "Fatima", "Arjun", "Chloe", "Leo", "Sofia", "Amir", "Elena", "Liam", "Emma", "Noah", "Olivia", "Oliver", "Ava", "Elijah", "Isabella", "William", "Sophia", "James", "Mia"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright"]
CITIES = [
    ("Paris", 48.8566, 2.3522),
    ("Marseille", 43.2965, 5.3698),
    ("Lyon", 45.7640, 4.8357),
    ("Toulouse", 43.6047, 1.4442),
    ("Nice", 43.7102, 7.2620),
    ("Nantes", 47.2184, -1.5536),
    ("Strasbourg", 48.5734, 7.7521),
    ("Montpellier", 43.6108, 3.8767),
    ("Bordeaux", 44.8378, -0.5792),
    ("Lille", 50.6292, 3.0573),
    ("Rennes", 48.1173, -1.6778),
    ("Reims", 49.2583, 4.0317)
]
BIOS = [
    "I love sharing my culture and language over a warm meal.",
    "Expat living in France for 5 years. Happy to show you around!",
    "Teacher by day, host by night. Come stay with me.",
    "Student studying abroad. Let's explore the city together.",
    "Foodie and travel enthusiast. I can give you the best restaurant recommendations.",
    "Musician looking to connect with people from all over the world.",
    "Artist with a spare room. My home is full of colors and good energy.",
    "Digital nomad settling down. Happy to share my space with fellow travelers.",
    "Local guide and historian. I'll tell you all the secrets of this city.",
    "Coffee lover and avid reader. Let's grab a cup and chat."
]

API = 'http://localhost:5000/api'

def generate_host(index):
    country_name, country_code, nationality, langs = random.choice(COUNTRIES)
    city_name, lat, lng = random.choice(CITIES)
    lat += random.uniform(-0.05, 0.05)
    lng += random.uniform(-0.05, 0.05)
    
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    email = f"host_{index}_{first.lower()}_{last.lower()}@example.com"
    
    return {
        'email': email,
        'password': 'password123',
        'profile': {
            'first_name': first,
            'last_name': last,
            'phone': f"+33 6 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}",
            'bio': random.choice(BIOS) + " Represents: " + country_name,
            'nationality': nationality,
            'nationality_code': country_code,
            'languages': langs.split(','),
            'address': f"{random.randint(1, 150)} Rue de {random.choice(FIRST_NAMES)}",
            'city': city_name,
            'country': 'France',
            'lat': lat,
            'lng': lng,
            'hosting_since': str(random.randint(2018, 2024)),
            'max_guests': random.randint(1, 4),
            'available': random.choice([True, True, True, False])
        }
    }

def seed_massive():
    print(f"Generating 1000 hosts from 195 countries...")
    hosts = [generate_host(i) for i in range(1000)]
    
    success, skipped, failed = 0, 0, 0
    
    for i, h in enumerate(hosts):
        email = h['email']
        res = requests.post(f'{API}/auth/register', json={'email': email, 'password': h['password']})
        
        if res.status_code == 409:
            skipped += 1
            if i % 50 == 0: print(f"Progress: {i}/1000...")
            continue
        elif res.status_code != 201:
            failed += 1
            continue
            
        token = res.json()['token']
        res2 = requests.post(f'{API}/profile', json=h['profile'], headers={'Authorization': f'Bearer {token}'})
        
        if res2.status_code == 201:
            success += 1
        else:
            failed += 1
            
        if i % 50 == 0:
            print(f"Progress: {i}/1000... (Success: {success})")
            
    print(f"\nFinal: {success} created, {skipped} skipped, {failed} failed.")

if __name__ == '__main__':
    try:
        requests.get(f'{API}/hosts', timeout=3)
    except requests.ConnectionError:
        print('Cannot reach backend. Make sure app_auth.py is running on port 5000.')
        exit(1)
    seed_massive()
