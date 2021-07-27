import json

from faker import Faker
from faker.providers import barcode
from faker.providers import phone_number
from faker.providers import isbn
from faker.providers import lorem
from faker.providers import ssn
from faker.providers import address

from src.utils import process_wards

fake = Faker()
fake.add_provider(barcode)
fake.add_provider(phone_number)
fake.add_provider(isbn)
fake.add_provider(lorem)
fake.add_provider(ssn)
fake.add_provider(address)

with open('src/raw_data/vietnam_flat.json', 'r') as f:
    data = json.load(f)
    ward_data = list(process_wards(data))

user_data = []

for i in range(200):
    first_name = fake.unique.first_name()
    last_name = fake.unique.last_name()
    phone_number = fake.phone_number()
    while len(phone_number) > 20:
        phone_number = fake.phone_number()
    fake.random.shuffle(ward_data)
    # Process communist/union
    communist_status = fake.random.choice([True, False])
    entry_date = None
    union_status = False
    union_date = None
    if communist_status:
        entry_date = int(fake.date_time_between(start_date='-10y',
                                                end_date='-2y').strftime('%s'))
        union_status = True
        union_date = int(fake.date_time_between(start_date='-20y',
                                                end_date='-10y').strftime('%s'))

    # Process working status
    working_status = fake.random.randint(2, 8)
    start_working_date = int(fake.date_time_between(start_date='-30y',
                                                    end_date='-10y').strftime(
        '%s'))
    end_working_date = None
    if working_status in {7, 8}:
        end_working_date = int(fake.date_time_between(start_date='-10y',
                                                      end_date='now').strftime('%s'))
    # Process teaching title, degree, academic
    degree = fake.random.randint(1, 6)
    academic_tile = None
    teaching_tile = None
    if degree in range(1, 5):
        teaching_tile = fake.random.randint(1, 4)
    elif degree in range(5, 7):
        teaching_tile = fake.random.randint(4, 7)
        academic_tile = fake.random.randint(1, 2)
    temp = {
        'code': f'VLU123{i + 1}',
        'type': fake.random.randint(0, 1),
        'first_name': first_name,
        'last_name': last_name,
        'gender': fake.random.randint(0, 2),
        'dob': int(fake.date_time_between(start_date='-50y',
                                          end_date='-22y').strftime('%s')),
        'work_email': f'{first_name.lower()}.{last_name.lower()}@vlu.edu.vn',
        'phone': phone_number,
        'tax_code': fake.isbn10(),
        'social_code': fake.isbn10(),
        'bio': fake.sentence(nb_words=8),
        'permission_profile_id': 1,
        'employment_contract_id': fake.random.randint(1, 5),
        'birth_place_id': fake.random.randint(1, 63),
        'home_town_id': fake.random.randint(1, 63),
        'ethnics_id': 1,
        'religion_id': fake.random.randint(1, 6),
        'gov_id': fake.ssn(),
        'gov_date_issue': int(fake.date_time_between(start_date='-20y',
                                                     end_date='-2y').strftime(
            '%s')),
        'gov_place_id': fake.random.randint(1, 63),
        'passport_id': fake.ssn(),
        'passport_date_issue': int(fake.date_time_between(start_date='-20y',
                                                          end_date='-2y').strftime(
            '%s')),
        'passport_place_id': fake.random.randint(1, 63),
        'permanent_address': fake.street_address(),
        'permanent_address_ward_id': ward_data[0].get('ward_code'),
        'permanent_address_district_id': ward_data[0].get('district_code'),
        'permanent_address_province_id': ward_data[0].get('province_code'),
        'mailing_address': fake.street_address(),
        'mailing_address_ward_id': ward_data[0].get('ward_code'),
        'mailing_address_district_id': ward_data[0].get('district_code'),
        'mailing_address_province_id': ward_data[0].get('province_code'),
        'communist_party_status': communist_status,
        'communist_party_entry_date': entry_date,
        'union_party_status': union_status,
        'union_party_entry_date': union_date,
        'working_status_id': working_status,
        'start_working_date': start_working_date,
        'end_working_date': end_working_date,
        'degree_id': degree,
        'teaching_title_id': teaching_tile,
        'academic_title_id': academic_tile
    }
    user_data.append(temp)


with open('output/user_data.json', 'w') as f:
    json.dump(user_data, f, ensure_ascii=False, indent=4)
