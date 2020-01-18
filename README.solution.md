Usage
-----

    #development
    $ ./setup.sh [docker-compose-file]

Access http://localhost:5000

    $ curl -Lk -X POST -H "Content-Type: multipart/form-data" -F "numbers=@numbers.csv" http://localhost:5000/locate_numbers > output.csv
    $ curl 'http://localhost:5000/locate_numbers/2134160509'

Ideas to improve process time
-----------------------------

    1. Load libphone data in memory:
        - phonenumbers.PhoneMetadata.load_all()
    2. Use DB/Memcached to save libphone replies

Dependencies
------------

- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
