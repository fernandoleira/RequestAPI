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


# Function to format the select section of the query
def format_selector(col, count_bool):
    sel = ""

    if count_bool:
        sel = "COUNT"
        if len(col) == 1:
            sel = sel + '(' + col[0] + ')'
        else:
            sel = sel + '(' + ", ".join(col) + ')'

    else:
        if len(col) == 1:
            sel = col[0]
        else:
            sel = '(' + ", ".join(col) + ')'

    return sel


# Function to return the elements
def single_elem_request(connection, tablename, column, elem_id, select_col, count_bool, limit_flag, offset_flag):
    arr = list()
    cur = connection.cursor()

    slc = format_selector(select_col, count_bool)

    qy = 'SELECT {0} FROM {1} WHERE {2} = {3}'.format(
        slc,
        tablename,
        column,
        str(elem_id)
    )

    if limit_flag is not None:
        qy += " LIMIT {}".format(limit_flag)

    if offset_flag is not None:
        qy += " OFFSET {}".format(offset_flag)

    qy += ';'
    cur.execute(qy)
    col_names = [desc[0] for desc in cur.description]
    rd = cur.fetchone()

    while rd is not None:
        elm = dict()
        rd = list(rd)
        cnt = 0
        for name in col_names:
            elm[name] = str(rd[cnt])
            cnt += 1

        arr.append(elm)
        rd = cur.fetchone()

    cur.close()
    if len(arr) == 1:
        return arr[0]
    else:
        return arr


# API Lambda function for the GET method
def lambda_handler(event, context):
    table_name = event["params"]["path"]["table"]
    col_name = event["params"]["path"]["col"]
    id_name = event["params"]["path"]["id"]

    if not id_name.isdigit():
        id_name = "'" + str(id_name) + "'"

    if "selectCol" not in event["params"]["querystring"]:
        select_cols = ['*']
    else:
        select_cols = eval(event["params"]["querystring"]["selectCol"])

    if "minID" not in event["params"]["querystring"]:
        event["params"]["querystring"]["minID"] = None

    if "maxID" not in event["params"]["querystring"]:
        event["params"]["querystring"]["maxID"] = None

    if "countReturn" not in event["params"]["querystring"]:
        event["params"]["querystring"]["countReturn"] = False

    if "limitFlag" not in event["params"]["querystring"]:
        event["params"]["querystring"]["limitFlag"] = None

    if "offsetFlag" not in event["params"]["querystring"]:
        event["params"]["querystring"]["offsetFlag"] = None

    # Test connection with the database
    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = single_elem_request(
        conn,
        table_name,
        col_name,
        id_name,
        select_cols,
        event["params"]["querystring"]["countReturn"],
        event["params"]["querystring"]["limitFlag"],
        event["params"]["querystring"]["offsetFlag"]
    )

    conn.close()
    return res
