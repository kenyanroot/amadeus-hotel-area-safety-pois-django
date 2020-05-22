import os
import requests


class Hotel:
    def __init__(self, hotel):
        self.hotel = hotel

    def construct_hotel(self):
        try:
            offer = {}
            offer['name'] = self.hotel['hotel']['name']
            offer['latitude'] = self.hotel['hotel']['latitude']
            offer['longitude'] = self.hotel['hotel']['longitude']
            offer['address'] = self.hotel['hotel']['address']['lines']
            offer['safety'] = self.safety(offer['latitude'], offer['longitude'])
        except (TypeError, AttributeError, KeyError):
            pass
        return offer
    
    def safety(self, lat, lng):
        GEOSURE_ACCESS_TOKEN = os.environ.get('GEOSURE_ACCESS_TOKEN')
        GEOSURE_ENDPOINT = os.environ.get('GEOSURE_ENDPOINT')
        parameters = {"latitude":lat,
                    "longitude": lng,
                    "access_token": GEOSURE_ACCESS_TOKEN
                    }

        safety = requests.get(url= GEOSURE_ENDPOINT,
                              params=parameters).json()

        overall = safety['data'][0]['safetyScores']['overall']
        overall_icon = self.classify_overall_safety_score(overall)
        lgbtq   = self.classify_safety_score(safety['data'][0]['safetyScores']['lgbtq'])
        theft   = self.classify_safety_score(safety['data'][0]['safetyScores']['theft'])
        medical = self.classify_safety_score(safety['data'][0]['safetyScores']['medical'])
        return f'<div><b>{overall}% Risk {overall_icon}</b></div>' \
               f'\n<b>LGBTQ</b>{lgbtq}' \
               f'\n<b>Theft</b> {theft}' \
               f'\n<b>Medical</b> {medical}'

    def classify_safety_score(self, score):
        if score <= 20:
            return '<div style="color:green;">Very safe</div>'
        elif 20 < score <= 40:
            return '<div style="color:yellow;">Safe</div>'
        elif 40 < score <= 60:
            return '<div style="color:orange;">Slight risk</div>'
        elif 60 < score <= 80:
            return '<div style="color:lightcoral;">Risk</div>'
        elif 80 < score <= 100:
            return '<div style="color:red;">High risk</div>'

    def classify_overall_safety_score(self, score):
        if score <= 20:
            return '&#129395'
        elif 20 < score <= 40:
            return '&#128578'
        elif 40 < score <= 60:
            return '&#129300'
        elif 60 < score <= 80:
            return '&#128556'
        elif 80 < score <= 100:
            return '&#128560'
