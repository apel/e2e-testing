"""
OIDC client-credentials token fetch.

Performs a single POST to a token endpoint using the OAuth2 client_credentials
grant. Never logs client secrets or returned token values.
"""

import requests

def generate_token(token_endpoint, client_id, client_secret):
    # type: (str, str, str) -> str
    """Fetch a bearer token via OAuth2 client_credentials grant.

    Args:
        token_endpoint (str): HTTPS URL of the token endpoint.
        client_id (str): OAuth2 client ID.
        client_secret (str): OAuth2 client secret.

    Returns:
        str: The access_token value from the response, or an error message
            if token generation fails.
    """

    # Define data dictionary
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "openid profile offline_access wlcg wlcg.groups storage.read:/ storage.write:/ storage.modify:/",
        "audience": "https://wlcg.cern.ch/jwt/v1/any"
    }

    # Attempt to retrieve token
    try:
        resp = requests.post(
            token_endpoint,
            data=data,
            verify=True,
            timeout=30,
        )
    except requests.exceptions.RequestException as exc:
        return("OIDC token request to {!r} failed: {}".format(token_endpoint, exc))

    # Return error message if token response was not ok
    if not resp.ok:
        return("OIDC token endpoint {!r} returned HTTP {}: {}".format(
            token_endpoint, resp.status_code, resp.text[:200],
        ))

    # Try to access the body of the response, if it exists
    try:
        body = resp.json()
    except ValueError as exc:
        return("OIDC token endpoint {!r} returned non-JSON response: {}".format(
            token_endpoint, exc
        ))

    # Try to return the access token, if it exists within the response body
    token = body.get("access_token")
    if not token:
        return("OIDC token endpoint {!r} response missing 'access_token'".format(
            token_endpoint
        ))

    return token
