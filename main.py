import requests
import json

class Bypass:
    def __init__(self) -> None:
        self.cookieToBypass = open("cookieToBypass.txt").read()
        self.yourOwnCookie = open("yourOwnCookie.txt").read()
    
    def start_process(self):
        self.xcsrf_token = self.get_csrf_token()
        self.rbx_authentication_ticket = self.get_rbx_authentication_ticket()
        return self.get_set_cookie()
        
    def get_set_cookie(self):
        
        headers = {
            "Content-Type": "application/json",  
            "rbxauthenticationnegotiation":1,  
            "user-agent":"Roblox/WinInet", 
            "origin":"https://www.roblox.com", 
            "referer":"https://www.roblox.com/my/account", 
            "x-csrf-token": self.csrf_token
        }
        body = {"authenticationTicket": self.rbx_authentication_ticket}
        
        response = requests.post("https://auth.roblox.com/v1/authentication-ticket/redeem", headers=headers, data=body)
        
        set_cookie_header = response.headers.get("set-cookie")
        if set_cookie_header is None:
            raise Exception("An error occurred while getting the set_cookie")
        
        return set_cookie_header.split(".ROBLOSECURITY=")[1].split(";")[0]

        
    def get_rbx_authentication_ticket(self):
        headers = {
            "Content-Type": "application/json", 
            "rbxauthenticationnegotiation": "1", 
            "user-agent": "Roblox/WinInet", 
            "origin": "https://www.roblox.com", 
            "referer": "https://www.roblox.com/my/account",
            "cookie": ".ROBLOSECURITY="+self.cookieToBypass, 
            "x-csrf-token": self.xcsrf_token
        }
    
        response = requests.post("https://auth.roblox.com/v1/authentication-ticket", headers=headers)
        print(response.json())
        if response.headers.get("rbx-authentication-ticket") is None:
            raise Exception("An error occurred while getting the rbx-authentication-ticket")
        
        return response.headers.get("rbx-authentication-ticket")
        
        
    def get_csrf_token(self) -> str:
        response = requests.post("https://accountsettings.roblox.com/v1/email", cookies = {".ROBLOSECURITY": self.yourOwnCookie})
        xcsrf_token = response.headers.get("x-csrf-token")
        if xcsrf_token is None:
            raise Exception("An error occurred while getting the X-CSRF-TOKEN. "
                            "Could be due to an invalid Roblox Cookie")
                 
        return xcsrf_token
    
print(Bypass().start_process())