import imaplib
import smtplib
import email
import json

f = open('balance.sfu', 'r')
data = json.loads(f.read())
f.close()

wu_api = data['weather_api']
gu = data['gmail']['user']
gp = data['gmail']['pass']

def get_msg():
    import requests
    import json
    
    req = "http://api.wunderground.com/api/"+wu_api+"/conditions/q/MI/48122.json"
    
    resp = requests.get(req)
    resp = resp.json['current_observation']
    
    msg = "It is %s at %s with humidity of %s (dewpoint: %s)." % (resp['icon'], resp['temperature_string'], resp['relative_humidity'], resp['dewpoint_string'])
    msg = "%s  %s are the winds," % (msg, resp['wind_string'])
    msg = "%s providing a wind chill of %s and heat index of %s." % (msg, resp['windchill_string'], resp['feelslike_string'])
    msg = "%s  Visibility is %s miles." % (msg, resp['visibility_mi'])
    msg = "%s  Data was fetched from %s at %s." % (msg, resp['observation_location']['full'], resp['local_time_rfc822'])
    
    return msg
    
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(gu, gp)
imap.select('inbox')

smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
smtp.login(gu, gp)

res, data = imap.uid('search', None, '((FROM "*.txt.voice.google.com") (UNSEEN))')

data = data[0].split()

body_msg = get_msg()

for msg_id in data:
    body = imap.uid('fetch', msg_id, '(RFC822)')[1][0][1]
    em = email.message_from_string(body)
    
    users, domain = email.utils.parseaddr(em['From'])[1].split('@')
    parts = users.split(".")
    
    to = "\"%s\" <%s.%s.%s@%s>" % (email.utils.parseaddr(em['From'])[0], parts[0], parts[1], parts[2], domain)
    
    # mark message for deletion, then do it
    imap.uid('STORE', msg_id, '+FLAGS', '(\Deleted)')
    imap.expunge()
    
    headers = ["From: " + em['From'], "Subject: SMS from %s" % (email.utils.parseaddr(em['From'])[0]),
               "To: "+to, "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    
    smtp.sendmail(em['From'], to, headers + "\r\n\r\n" + body_msg)