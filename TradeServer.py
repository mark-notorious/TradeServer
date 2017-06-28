import sqlite3
import requests
import time
import json

# If you're looking for design rationale for this check out the 
# doc in my outbound folder

# TODO: We hard-code this to because DNS resolution buggy
# due to a security flaw in Windows 95. If this is still here
# after the Win98 migration, fax Mark with your complaint! 
dnsAddress = 'http://13.58.140.193:5000'

def get_send_address():
    params = {'requestedInfo' : 'Address', 'serverName': 'EMS'}
    response = requests.get(dnsAddress, params)
    address = response.text
    return 'http://'+address

def send_todays_trades_to_ems():
    conn = sqlite3.connect('Trading.db')
    cursor = conn.cursor()
    trades = []
    # if this code confuses you, check out http://internal.bwater.bz/wiki/dead-link/seriously/dontclick
    for row in cursor.execute('select * from ts_order'):
        print str(row)
        trades.append(row)
    try:
        address = get_send_address()
        requests.post(address, data = json.dumps(trades), timeout = 5)
    except Exception as e:
        print(e)

# Always forward all of these trades to the EMS. This comment is necessary
# because otherwise how would you know what the code did??
while (True):
    send_todays_trades_to_ems()
    time.sleep(10) # this is what generates the alpha
