import requests
import json
import datetime


CURRENT_DATE = datetime.datetime.today().strftime('%Y-%m-%d')
COUNT_FLAG = True
LIMIT_FLAG = 10
OFFSET_FLAG = 1


# ======================================== GET REQUEST =========================================



# Index
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    },
    
)

print(get_req.status_code)
print(get_req.headers)
print(get_req.text)


# Show
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/emp_no/10001",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(get_req.status_code)
print(get_req.headers)
print(get_req.text)




# ======================================== POST REQUEST ========================================



# Get the last element id
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

last_elem_id = str(int(list(json.loads(get_req.text))[-1]["emp_no"]) + 1)


# New element to insert
new_elems = [
    {
        "emp_no": last_elem_id,
        "birth_date": "'1998-12-05'",
        "first_name": "'Fernando'",
        "last_name": "'Leira'",
        "gender": "'M'",
        "hire_date": "'{}'".format(CURRENT_DATE)
    },
    {
        "emp_no": str(int(last_elem_id) + 1),
        "birth_date": "'1998-12-05'",
        "first_name": "'Fern'",
        "last_name": "'Leira'",
        "gender": "'M'",
        "hire_date": "'{}'".format(CURRENT_DATE)
    }
]

# Create
post_req = requests.post("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees",
    json=new_elems,
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(post_req.status_code)
print(post_req.headers)
print(post_req.text)



# ======================================== PATCH REQUEST ========================================



# Element columns to update
update_elem = {
    "first_name": "'John'",
    "last_name": "'Smith'"
}

# Update
patch_req = requests.patch("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/10115",
    json=update_elem,
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(patch_req.status_code)
print(patch_req.headers)
print(patch_req.text)



# ======================================== DELETE REQUEST ======================================



# Destroy
delete_req = requests.delete("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/10115",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(delete_req.status_code)
print(delete_req.headers)
print(delete_req.text)



# ========================================= HEAD REQUEST =======================================



head_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(head_req.text)



# ======================================== TABLE REQUEST =======================================



new_table = {
    "table-name": "NewTable",
    "columns": [
        {
            "title": "Id",
            "type": "int",
            "null": False,
            "primary-key": True
        },
        {
            "title": "LastName",
            "type": "varchar(255)",
            "null": False
        },
        {
            "title": "FirstName",
            "type": "varchar(255)",
            "null": False
        },
        {
            "title": "Address",
            "type": "varchar(255)",
            "null": False
        },
        {
            "title": "City",
            "type": "varchar(255)",
            "null": False
        },
        {
            "title": "State",
            "type": "varchar(255)",
            "null": False
        },
        {
            "title": "ZipCode",
            "type": "int",
            "null": False
        }
    ]
}

table_req = requests.post("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db",
    json=new_table,
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(table_req.status_code)
print(table_req.headers)
print(table_req.text)

