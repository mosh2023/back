import requests as req


resp = req.put('http://127.0.0.1:5002/v1/player/join',
    json={
        'user_id': 2,
        'key': 'ABClasses'
    })
print(resp)
print(resp.content)
