# These will change after set
API_TOKEN = ""
IP = ""

# file name
TOKEN_FILE = "api_token.json"
IP_FILE = "ip.json"
WORK_FILE = "work.json"

# status code
SUCCESS_STATUS_CODE = 200

# Create v1 api token params
VALIDITY_PERIOD = 0  # token期限永久
TOKEN_SCOPES = ["edit:user", "edit:space", "edit:visitor",
                "edit:credential", "view:system_log", "edit:policy", "edit:device"]

# Get logs params
TOPIC = "door_openings"  # 目前只會用到這個功能，其餘可參考unifi access token (Topic Reference)
