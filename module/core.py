from typing import Any
from flask import request, jsonify, make_response, Response

def getRequestParameter(request: request) -> dict:
    data = {}
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
    return dict(data)

class GenerateResponse:
    def __init__(self) -> None:
        self.code = 0
        self.message = ''
        self.data = None
        self.httpCode = 200

    def generate(self) -> Response:
        responseJson = jsonify({
            'code': self.code,
            'message': self.message,
            'data': self.data
        })
        response_ = make_response(responseJson)
        response_.status_code = self.httpCode
        response_.mimetype = 'application/json; charset=utf-8'
        return response_

    def error(self, code: int, message: str, httpCode=200) -> Response:
        self.code = code
        self.message = message
        self.httpCode = httpCode
        return self.generate()

    def success(self, data: Any) -> Response:
        self.code = 200
        self.message = 'success'
        self.data = data
        return self.generate()

class State:
    WAIT = 0
    ING = 1
    SUCCESS = 2
    FAIL = 3