class Body(BaseModel):
    length: Union[int, None] = DEFAULT_LENGTH
    text: str


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    try:
        string = base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
    except Exception as e:
        return {'error': str(e)}
    return {'token': string}


@app.post('/checksum')
def checksum(body: Body):
    """
    Generate a checksum of the text. Example POST request body:

    {
        "text": "Hello World!"
    }
    """
    try:
        checksum = hashlib.sha256(body.text.encode('utf-8')).hexdigest()
    except Exception as e:
        return {'error': str(e)}
    return {'checksum': checksum}