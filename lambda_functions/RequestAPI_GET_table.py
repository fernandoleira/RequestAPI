import os
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


def format_selector(col, count_flag):
    sel = ""

    if count_flag:
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


def all_elem_request(
        connection,
        tablename,
        select_col,
        where_column,
        min_id,
        max_id,
        count_flag,
        limit_flag,
        offset_flag):
    arr = list()
    cur = connection.cursor()

    slc = format_selector(select_col, count_flag)

    qy = 'SELECT {0} FROM {1}'.format(slc, tablename)

    if where_column is not None:
        if min_id is not None and max_id is not None:
            qy += " WHERE {0} > {1} AND {0} < {2}".format(where_column, min_id, max_id)
        elif min_id is not None:
            qy += " WHERE {0} > {1}".format(where_column, min_id)
        elif max_id is not None:
            qy += " WHERE {0} < {1}".format(where_column, max_id)

    if limit_flag is not None:
        qy += " LIMIT {}".format(limit_flag)

    if offset_flag is not None:
        qy += " OFFSET {}".format(offset_flag)

    qy += ';'
    cur.execute(qy)

    col_names = [desc[0] for desc in cur.description]

    rd = cur.fetchone()
    while rd is not None:
        rd = list(rd)
        assets = dict()
        for name in col_names:
            assets[name] = ""

        cnt = 0
        for key in assets.keys():
            assets[key] = str(rd[cnt])
            cnt += 1

        arr.append(assets)
        rd = cur.fetchone()

    cur.close()
    return arr


# API Lambda function for the GET method
def lambda_handler(event, context):
    table_name = event["params"]["path"]["table"]

    if "selectCol" not in event["params"]["querystring"]:
        select_cols = ['*']
    else:
        select_cols = eval(event["params"]["querystring"]["selectCol"])

    if "whereColumn" not in event["params"]["querystring"]:
        event["params"]["querystring"]["whereColumn"] = None

    if "minID" not in event["params"]["querystring"]:
        event["params"]["querystring"]["minID"] = None

    if "maxID" not in event["params"]["querystring"]:
        event["params"]["querystring"]["maxID"] = None

    if "countFlag" not in event["params"]["querystring"]:
        event["params"]["querystring"]["countFlag"] = False
    else:
        event["params"]["querystring"]["countFlag"] = bool(event["params"]["querystring"]["countFlag"])

    if "limitFlag" not in event["params"]["querystring"]:
        event["params"]["querystring"]["limitFlag"] = None

    if "offsetFlag" not in event["params"]["querystring"]:
        event["params"]["querystring"]["offsetFlag"] = None

    try:
        test_connection = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))
        test_connection.close()
    except ImportError:
        return "Could not connect to the database"

    conn = db_connection(os.environ.get("DB_USERNAME"), os.environ.get("DB_PASSWORD"))

    res = all_elem_request(
        conn,
        table_name,
        select_cols,
        event["params"]["querystring"]["whereColumn"],
        event["params"]["querystring"]["minID"],
        event["params"]["querystring"]["maxID"],
        event["params"]["querystring"]["countFlag"],
        event["params"]["querystring"]["limitFlag"],
        event["params"]["querystring"]["offsetFlag"],
    )

    conn.close()

    if len(res) == 1:
        return res[0]

    return res
