import requests
import json
import datetime


CURRENT_DATE = datetime.datetime.today().strftime('%Y-%m-%d')


# ======================================== GET REQUEST =========================================

# Index
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(get_req.status_code)
print(get_req.headers)
print(get_req.text)

# Show
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/10001",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(get_req.status_code)
print(get_req.headers)
print(get_req.text)

# ======================================== POST REQUEST ========================================

get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees", 
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

last_elem_id = str(int(list(json.loads(get_req.text))[-1]["emp_no"]) + 1)

new_elem = {
    "emp_no": last_elem_id, 
    "birth_date": "'1998-12-05'",
    "first_name": "'Fernando'",
    "last_name": "'Leira'",
    "gender": "'M'",
    "hire_date": "'{}'".format(CURRENT_DATE)
}

post_req = requests.post("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees",
    json=new_elem,
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(post_req.status_code)
print(post_req.headers)
print(post_req.text)

# ======================================== PATCH REQUEST ========================================

update_elem = {
    "first_name": "'John'",
    "last_name": "'Smith'"
}

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

delete_req = requests.delete("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/10115",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(delete_req.status_code)
print(delete_req.headers)
print(delete_req.text)
