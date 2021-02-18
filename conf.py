# configurations...

# Address to Listening
BIND_ADDR = "0.0.0.0"
# DEbug Flags
DEBUG = False

ADMIN = {
  "id": "admin",
  "pw": "password_here"
}


# IP based restriction
DENYED_FROM = [
	"0.0.0.0/0", # Deny from ALL
]
ALLOWED_FROM = [
	"1.2.3.4/32", # Accept From Only
]
