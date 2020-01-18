from flask import redirect, url_for, request
from phonenumbers import geocoder

import phonenumbers
from . import app

PHONE_REGION = "US"

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/index.html', methods=['GET'])
def index():
    return """Usage:

    $ curl -i -X POST -H 'Content-Type: multipart/form-data' -F 'numbers=@numbers.csv' {}locate_numbers
    $ curl {}locate_numbers/2134160509
    """.format(request.url, request.url), 200, {'Content-Type': 'text/plain'}

@app.route('/locate_numbers', methods=['GET', 'POST'])
def locate_numbers():
    if request.method == 'POST':
        if 'numbers' not in request.files:
            return redirect(url_for('index'))

        numbers = request.files['numbers'].readlines()
        numbers_results = []

        for line in numbers:
            line = line.rstrip().decode()
            number = format_phonenumber(line)

            if number == 'numbers':
                number_result = [line, 'valid', 'location']
            else:
                try:
                    parsed_number = phonenumbers.parse(number, PHONE_REGION)
                    if phonenumbers.is_valid_number(parsed_number):
                        location = geocoder.description_for_number(parsed_number, "en")
                        number_result = [line, 'true', location]
                    else:
                        number_result = [line, 'false', 'n/a']
                except:
                    number_result = [line, 'false', 'n/a']

            numbers_results.append(number_result)

        return '\n'.join(', '.join(elems) for elems in numbers_results), 200, {'Content-Type': 'text/plain'}

    else: # request.method == 'GET'
        msg = "HTTP 501: Not implemented"
        return msg, 501, {'Content-Type': 'text/plain'}

@app.route('/locate_numbers/<number>', methods=['GET'])
def locate_number(number):
    formated_number = format_phonenumber(number)
    parsed_number = phonenumbers.parse(formated_number, PHONE_REGION)

    app.logger.debug(parsed_number)

    if phonenumbers.is_valid_number(parsed_number):
        location = geocoder.description_for_number(parsed_number, "en")
        nearby_number = find_nearby_number(formated_number, location)
        msg = "{} and {} are both a '{}' number".format(number, nearby_number, location)
        status = 200
    else:
        msg = "Invalid number: {}".format(number)
        status = 201

    return msg, status, {'Content-Type': 'text/plain'}

def format_phonenumber(number):
    #input  => (213) 416-0509
    #output => 2134160509
    return number.translate({ord(i):None for i in '()- '})

def find_nearby_number(formated_number, location):
    with open('numbers.csv') as f:
        numbers = [line.rstrip() for line in f]

    for number in numbers:
        iter_formated_number = format_phonenumber(number)

        if iter_formated_number == formated_number:
            continue

        try:
            parsed_number = phonenumbers.parse(number, PHONE_REGION)
            if phonenumbers.is_valid_number(parsed_number):
                iter_location = geocoder.description_for_number(parsed_number, "en")

            if location == iter_location:
                break
        except:
            continue

    return number
