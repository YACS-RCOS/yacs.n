# User
## GET /user
Get the profile of the current user using current session id.
### Request
#### Header
```
application/json
```
#### Body
```json
{
    "sessionID" : "f94e7cd0-6e10-11ea-8a3d-000d3a185820"
}
```
### Response
#### Header
```
application/json
```
#### Body
```json
{
    success: true
    errMsg: null,
    content: 
    {
        "uid": "4",
        "name": "John",
        "email": "aaa@wa.com",
        "phone": "51829838475",
        "major": "CS",
        "degree": "Undergraduate"
    } 
}
```
## PUT /user
Update the profile of the current user.
### Request
#### Header
```
application/json
```
#### Body
```json
{
    "sessionID": "213123-123-123-213-3123",
    "name": "John",
    "email": "aaa@wa.com",
    "phone": "51829838475",
    "major": "CS",
    "newPassword" : "new123456",
    "degree": "Undergraduate"
}
```
### Response
#### Header
```
application/json
```
#### Body
```json
{
    success: true
    errMsg: null,
    content: {}
}
```
## POST /user
Create a new user.
### Request
#### Header
```
application/json
```
#### Body
```json
{
    "name": "John",
    "email": "aaa@wa.com",
    "phone": "51829838475",
    "major": "CS",
    "password" : "123456",
    "degree": "Undergraduate"
}
```
### Response
#### Header
```
application/json
```
#### Body
```json
{
    success: true
    errMsg: null,
    content: 
    {
        "msg": "User added successfully"
    }
}
```
## DELETE /user
Delete current user.
### Request
#### Header
```
application/json
```
#### Body
```json
{
    "sessionID": "12312-321-3-12-3",
    "password" : "123456"
}
```
### Response
#### Header
```
application/json
```
#### Body
```json
{
    success: true
    errMsg: null,
    content: 
    {   
        "uid": "213-2-321-3-12-3",
        "msg": "Failed to delete user."
    }
}
```

# Session
## POST /session
Log in the user account and create the session.
### Request
#### Header
```
application/json
```
#### Body
```json
{
	"email" : "test@gmail.com",
	"password" : "testtest"
}
```
### Response
#### Header
```
application/json
```
#### Body
```json
{
  "success": true,
  "errMsg": null,
  "content": {
    "sessionID": "d635029a-6e16-11ea-b53e-000d3a185820",
    "startTime": "2020-03-24 21:31:35.035596",
    "uid": 2
  }
}
```

## DELETE /session
Log out the user account and end the session.
### Request
#### Header
```
application/json
```
#### Body
```json
{
	"sessionID" : "d635029a-6e16-11ea-b53e-000d3a185820"
}
```
### Response
#### Header
```
application/json
```
#### Body
```json
{
  "success": true,
  "errMsg": null,
  "content": {
    "endTime": "2020-03-24 21:34:24.369808",
    "sessionID": "d635029a-6e16-11ea-b53e-000d3a185820"
  }
}
```