import balanced
import sys
import json
import datetime

f = open('balance.sfu', 'r')
api_key = json.loads(f.read())
f.close()

api_key = api_key['token']['testing']

def get_trans_type(transaction_number):
     type = {
         'H': {'type': "Hold", 'handle' : balanced.Hold},
         'W': {'type': "Debit", 'handle' : balanced.Debit}, 
         'C': {'type': "Credit", 'handle' : balanced.Credit}
     }[transaction_number[0]]
     
     return type

"""
def fmt_currency(val):
    tmp = val
    
    if not isinstance(tmp, str):
        tmp = str(tmp)
    
    if val < 100:
        cents = tmp
        dollars = "0"
    else:
        cents = tmp[-2:]
        dollars = tmp[0:len(tmp)-2]
    
    return "%s.%s" % (dollars, cents)
"""
def fmt_currency(val):
    return '$%.02f' % (val/100.)

try:
	trans_num = sys.argv[1]
except:
	trans_num = raw_input("Enter transaction ID: ")

balanced.configure(api_key)

trans_info = get_trans_type(trans_num)

try:
    trans = balanced.Debit.query.filter(trans_info['handle'].f.transaction_number==trans_num).one()
    src = trans.source
    acct = trans.account
except:
    sys.exit("No transaction by ID %s exists." % (trans_num))
    
print "Transaction Details"
print "-------------------"
print "ID:", trans_num
print "Type:", trans_info['type']
print "Description:",trans.description
print "Appearing on statement as:",trans.appears_on_statement_as
print "Charge Amount:",fmt_currency(trans.amount)
print "Fees to Balanced:",fmt_currency(trans.fee)
print "Created At:",trans.created_at

print "\nAccount Details"
print "---------------"
print "Name:",acct.name
print "E-mail:", acct.email_address
print "\nSource Details"
print "----------------"
print "Card Holder:",src.name
print "Last Four:",src.last_four
print "Brand:", src.brand
print "Expiration: %s/%s" % (src.expiration_month, src.expiration_year)
print "Hash:",src.hash
