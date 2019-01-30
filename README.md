# RequestAPI

RequestAPI is a Python project built in the AWS API Gateway platform that handles request to a PostgreSQL database.

## Usage

Here are some examples with different HTTP methods

### GET DB

Return the database and tables information

```python
import requests

head_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(head_req.status_code)
print(head_req.headers)
print(head_req.text)
```

### POST DB

Write a new table in JSON and push it into the database.

```python
import requests

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
```

### GET TABLE

Return all of the rows in the table (Index) or an specific one (Show).

```python
import requests

# Index
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(get_req.status_code)
print(get_req.headers)
print(get_req.text)
```

### GET ELEMENT

```python
import requests

# Return employee with number '10001'
get_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/10001",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(get_req.status_code)
print(get_req.headers)
print(get_req.text)
```

### POST TABLE 

Insert a new row into a table.

```python
import requests
import json
import datetime

CURRENT_DATE = datetime.datetime.today().strftime('%Y-%m-%d') # Get current date

# New elements to insert
new_elems = [
    {
        "birth_date": "'1998-12-05'",
        "first_name": "'Fernando'",
        "last_name": "'Leira'",
        "gender": "'M'",
        "hire_date": "'{}'".format(CURRENT_DATE)
    },
    {
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
```

### PATCH ROW

Update a row and push it to the table.

```python
import requests

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
```

### DELETE ROW

Delete a row from a table.

```python
import requests

# Destroy
delete_req = requests.delete("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db/employees/10115",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI",
    }
)

print(delete_req.status_code)
print(delete_req.headers)
print(delete_req.text)
```

### Flags

```python
COUNT_FLAG = True
LIMIT_FLAG = 10
OFFSET_FLAG = 1
```