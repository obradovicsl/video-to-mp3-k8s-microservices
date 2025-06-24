import os, requests

def login(request):
    try:
        auth = request.authorization
        if not auth:
            return None, ("missing credentials", 401)
        
        basicAuth = (auth.username, auth.password)

        response = requests.post(
            f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
        )

        if response.status_code == 200:
            return response.text, None
        return None, (response.text, response.status_code)
    except Exception as err:
        return None, (f"unusual error: {err}", 500)