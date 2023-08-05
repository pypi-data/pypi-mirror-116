import hashlib
import json
from dpkt import http, UnpackError
from .MyEncoder import MyEncoder


class HttpData:
    def __init__(self):
        self.request = None
        self.response = None
        self.fileHashes = None

    def getDomain(self):
        if self.request.headers:
            if "host" in self.request.headers and self.request.headers["host"]:
                return self.request.headers["host"].strip()
        return ""

    def getUrl(self):
        return f"http://{self.getDomain()}{self.request.uri}"

    def __repr__(self):
        request = self.request
        response = self.response
        if request is None:
            return "None"
        requestDict = {

        }
        if request is not None:
            requestDict = {
                "uri": request.uri,
                "method": request.method,
                "headers": request.headers,
                "version": request.version,
                "body": request.body,
            }
        responseDict = {

        }
        if response is not None:
            responseDict = {
                "status": response.status,
                "reason": response.reason,
                "body": response.body,
                "headers": response.headers,
                "version": response.version,
            }
        return json.dumps({
            "request": requestDict,
            "response": responseDict,
            "fileHash": self.fileHashes
        }, ensure_ascii=False, cls=MyEncoder)


class HTTPParser:
    def parse(self, requestBytes, responseBytes: bytes) -> [HttpData]:
        # extract request
        startIdx = 0
        requests, responses = [], []
        while startIdx < len(requestBytes):
            try:
                http_req = http.Request(requestBytes[startIdx:])
                # http_req.headers = dict(http_req.headers)
                startIdx += len(http_req.__bytes__())
                requests.append(http_req)
            except UnpackError as e:
                # print(e)
                return []
        # extract response
        if len(requests) == 0:
            return []
        startIdx = 0
        while startIdx < len(responseBytes):
            try:
                http_response = http.Response(responseBytes[startIdx:])
                startIdx += len(http_response.__bytes__())
                responses.append(http_response)
            except UnpackError as e:
                # print(e)
                return []
        if len(requests) != len(responses):
            print(f"Request num: {len(requests)}, Response num: {len(responses)}, Not match")
            return []
        httpDataArr = []
        for i, http_req in enumerate(requests):
            httpData = HttpData()
            httpData.request = http_req
            httpData.response = responses[i]
            if 'content-type' in httpData.response.headers:
                contentType = httpData.response.headers['content-type'].strip()
                if contentType.startswith("image") or contentType.startswith("audio") or contentType.startswith(
                        "video") or \
                        contentType.startswith("application"):
                    httpData.fileHashes = {
                        "md5": hashlib.md5(httpData.response.body).hexdigest(),
                        "sha1": hashlib.sha1(httpData.response.body).hexdigest(),
                        "sha256": hashlib.sha256(httpData.response.body).hexdigest()
                    }
                    httpData.response.body = "It's a file, already cal file hashes"
            httpDataArr.append(httpData)
        return httpDataArr
