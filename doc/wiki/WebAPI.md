## Submit
### Request
1. Url: /submit.
2. Method: POST.
3. Format: Form.
4. Parameter:

Name|Type|Require|Illustrate
---|---|---|---
target|File|Yes|
source|File|No|Require when mode contains replace
modes|List|Yes|Only fill in replace,enhance
keepFPS|Number|No|Can be filled in when the mode contains replace,0 represents false,1 represents true
skipAudio|Number|No|Can be filled in when the mode contains replace,0 represents false,1 represents true
manyFace|Number|No|0 represents false,1 represents true
### Response
1. Format: JSON.
2. Parameter:

Name|Type|Illustrate
---|---|---
code|Integer|
message|String|
data|String|Token
3. Example:
```json
{
    "code": 200,
    "message": "success",
    "data": "1c40f444-716d-4159-a1f5-063dd0bf3978"
}
```
## Delete
### Request
1. Url: /delete.
2. Method: GET/POST.
3. Format: JSON(When the method is POST).
4. Parameter:

Name|Type|Require|Illustrate
---|---|---|---
token|String|Yes|
### Response
1. Format: JSON.
2. Parameter:

Name|Type|Illustrate
---|---|---
code|Integer|
message|String|
data|String|
3. Example:
```json
{
    "code": 200,
    "message": "success",
    "data": "success"
}
```
## Get State
### Request
1. Url: /get_state.
2. Method: GET/POST. 
3. Format: JSON(When the method is POST).
4. Parameter:

Name|Type|Require|Illustrate
---|---|---|---
token|String|Yes|
### Response
1. Format: JSON.
2. Parameter:

Name|Type|Illustrate
---|---|---
code|Integer|
message|String|
data|Number|
3. Example:
```json
{
    "code": 200,
    "message": "success",
    "data": 0
}
```
## Download
### Request
1. Url: /download.
2. Method: GET.
3. Parameter:

Name|Type|Require|Illustrate
---|---|---|---
token|String|Yes|
### Response
Format: Binary.