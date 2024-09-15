import msal

client_id = "80567770-d820-430e-9c29-fb27232364ae"
tenant_id = "c643d250-0dd7-416f-889e-a93f0e4ef800"
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = [f"api://{client_id}/user.read"]

# Create a public client application
app = msal.PublicClientApplication(client_id, authority=authority)

# Interactive user login
result = app.acquire_token_interactive(scopes=scope)

if "access_token" in result:
    print("Access token:", result["access_token"])
else:
    print("Error obtaining token:", result.get("error_description"))
