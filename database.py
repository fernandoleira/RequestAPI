import psycopg2


def connect():
    with open("keys.txt") as fn:
        password = fn.read()

    conf_params = {
        "host": "localhost",
        "database": "dvdrental",
        "user": "postgres",
        "password": password
    }

    try:
        conn = psycopg2.connect(**conf_params)
    except ImportError:
        print("Couldn't connect to the database")
        exit()

    print("Database Connected.")
    return conn

