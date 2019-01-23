import os
import json
import psycopg2

# PostgreSQL configuration parameters
DB_CONF_PARAMS = {
    "host": os.environ.get("DB_HOST"),
    "port": int(os.environ.get("DB_PORT")),
    "database": os.environ.get("DB_NAME"),
    "user": "",
    "password": ""
}


# Function to define and export the database connection configuration
def db_connection(username, password):
    DB_CONF_PARAMS["user"] = username
    DB_CONF_PARAMS["password"] = password

    conn = psycopg2.connect(**DB_CONF_PARAMS)
    return conn


def format_query(db_cols):
    res = ""

    for col in db_cols:
        res += "{0} {1} ".format(col["title"], col["type"].upper())

        if "primary-key" in col and col["primary-key"] == True:
            res += "PRIMARY KEY "

        if col["null"] == False:
            res += "NOT NULL"

        res += ', '

    return res[:-2]


# Function to push a "CREATE TABLE" query into the database
def create_table_request(connection, table_name, table_cols):
    cur = connection.cursor()

    qy = format_query(table_cols)

    cur.execute('CREATE TABLE {0} ({1});'.format(
        table_name,
        qy
    ))

    sm = cur.statusmessage

    cur.close()
    return sm


def lambda_handler(event, context):
    new_table_name = event["body-json"]["table-name"]
    new_table_cols = event["body-json"]["columns"]

    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = create_table_request(conn, new_table_name, new_table_cols)

    conn.commit()
    conn.close()

    return res
