# Game Recommendation Service.
Simple service that:
- handles user's requests
- has machine learning algorithms to find the best content for each user.
- allows user to register and login for personalized content
___
## How to use?
Since there is no interface you can simply send requests - allowed requests are
listed down below. For this you can use applications like `Postman`.
___
## User requests
### Register
Example:
```json
{
    "type": "register",
    "sender": "foo",
    "receiver": "bar",
    "content" : {
        "email": "foo@bar.com",
        "username": "foo",
        "password": "bar",
        "age": 42 
    }
}
```
### Login
Example:
```json
{
    "type": "login",
    "sender": "foo",
    "receiver": "bar",
    "content" : {
        "username": "foo",
        "password": "bar",
    }
}
```
## Server requests
The requests between servers look like this:
### API request
This is the base of every request that goes around between servers:
```json
{
    "id": "It is held locally and is synced with database",
    "type": "Depends on what type of request",
    "sender": "This is swapped with server IP for verification",
    "receiver": "Destination server",
    "timestamp": "When source server received it",
    "message_status": "Usually pending, but if request is correct it will be
    swapped with finished",
    "content" : "Depends on what type of request"
}
```
## Video request
This is derived from the `API Request`
```json
{
    ...
    "type": "video_fetch",
    ...
    "content": [ ... ]
}
```
