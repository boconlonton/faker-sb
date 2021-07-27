import json


def process_wards(data):
    """Returns a generator of dictionaries that contains ward information

    Args:
        data (Mapping): A dictionary of wards data
    """
    return (
        {
            'name': ward.get('ward_name'),
            'ward_code': ward.get('ward_code'),
            'district_code': ward.get('district_code'),
            'province_code': ward.get('province_code')
        }
        for ward in data
        if ward.get('ward_name')
    )
