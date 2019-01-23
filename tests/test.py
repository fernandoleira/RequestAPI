import requests


head_req = requests.get("https://atbqxoh3y8.execute-api.us-east-1.amazonaws.com/comp/db",
    headers={
        "x-api-key": "i25gWWDscH3MSE4utckN09vtGWfdaoBM7Bo6GXiI"
    }
)

print(head_req.text)