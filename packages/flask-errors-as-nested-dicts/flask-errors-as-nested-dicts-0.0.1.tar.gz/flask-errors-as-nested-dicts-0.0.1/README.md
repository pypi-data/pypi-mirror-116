# Flask Errors as Nested Dicts
This extension was developed for personal use and changes standard flask and jwt response errors to nested dicts, i. e.


```javascript
{
  "code": 404,
  "status": "Not Found"
}
```

to:

```javascript
{
  "errors": {
    "json": {
      "url": [
        "Does not exist."
      ]
    }
  }
}
```

Installing
----------

Install and update using pip:

```bash
$ pip install flask-errors-as-nested-dicts
```

Usage
----------------

```python
from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)
ErrorsAsNestedDicts(app, jwt)

```