import base64
import hashlib
import http.server
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser
import json


KEYCLOAK = "http://localhost:8080"
REALM = "know-your-dharma"
CLIENT_ID = "kyd-web"
REDIRECT_URI = "http://localhost:3000/callback"

AUTH_URL = (
    f"{KEYCLOAK}/realms/{REALM}/protocol/openid-connect/auth"
)

TOKEN_URL = (
    f"{KEYCLOAK}/realms/{REALM}/protocol/openid-connect/token"
)

code_verifier = secrets.token_urlsafe(64)

code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b"=").decode()

result = {}


class CallbackHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return

        params = urllib.parse.parse_qs(parsed.query)

        if "error" in params:
            result["error"] = params["error"][0]
            result["error_description"] = params.get(
                "error_description", [""]
            )[0]
        else:
            result["code"] = params["code"][0]

        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        self.wfile.write(
            b"""
            <html>
            <body>
                <h2>Authentication successful.</h2>
                <p>You can close this browser tab.</p>
            </body>
            </html>
            """
        )

    def log_message(self, format, *args):
        pass


server = http.server.HTTPServer(
    ("localhost", 3000),
    CallbackHandler,
)

thread = threading.Thread(
    target=server.handle_request,
    daemon=True,
)

thread.start()

params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": "openid profile email",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}

authorization_url = (
    AUTH_URL
    + "?"
    + urllib.parse.urlencode(params)
)

print()
print("Opening Keycloak...")
print()
print(authorization_url)
print()

webbrowser.open(authorization_url)

thread.join()

if "error" in result:
    print("Authentication failed:")
    print(result)
    server.server_close()
    raise SystemExit(1)

authorization_code = result["code"]

token_data = urllib.parse.urlencode({
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "code": authorization_code,
    "redirect_uri": REDIRECT_URI,
    "code_verifier": code_verifier,
}).encode()

request = urllib.request.Request(
    TOKEN_URL,
    data=token_data,
    method="POST",
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
    },
)

try:
    with urllib.request.urlopen(request) as response:
        token_response = json.loads(
            response.read().decode()
        )

except urllib.error.HTTPError as e:
    print("Token exchange failed:")
    print(e.read().decode())
    server.server_close()
    raise SystemExit(1)

server.server_close()

print()
print("=" * 70)
print("TOKEN CLAIMS")
print("=" * 70)

access_token = token_response["access_token"]

print()
print("ACCESS TOKEN FOR LOCAL TESTING:")
print(access_token)

try:
    parts = access_token.split(".")

    if len(parts) != 3:
        raise ValueError("Access token is not a JWT")

    payload = parts[1]

    # Restore JWT base64 padding
    payload += "=" * (-len(payload) % 4)

    claims = json.loads(
        base64.urlsafe_b64decode(payload)
    )

    selected_claims = {
        "iss": claims.get("iss"),
        "sub": claims.get("sub"),
        "aud": claims.get("aud"),
        "azp": claims.get("azp"),
        "exp": claims.get("exp"),
        "iat": claims.get("iat"),
        "scope": claims.get("scope"),
        "realm_access": claims.get("realm_access"),
    }

    print(
        json.dumps(
            selected_claims,
            indent=2,
        )
    )

except Exception as exc:
    print(f"Could not decode access token: {exc}")

print()
print("Authentication flow completed successfully.")