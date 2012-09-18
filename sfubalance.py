#!/usr/bin/env python

import balanced
import sys
import datetime

class Balance:
    def __init__(self):
        import json
        
        # To keep the API key a secret while still being able to showcase this script, a config script is used instead
        f = open('balance.sfu', 'r')
        self.api_key = json.loads(f.read())
        f.close()
        
        self.key = self.api_key['token']['testing']
        balanced.configure(self.key)
        
    def addCC(self, name, number, exp_month, exp_year, cvv):
        card = None
        
        try:
            card = balanced.Marketplace.my_marketplace.create_card(
                                                                   name=name,
                                                                   card_number=number,
                                                                   expiration_month=exp_month,
                                                                   expiration_year=exp_year,
                                                                   security_code=cvv)
        except Exception as e:
            if e.status_code == 400:
                print e.description
            elif e.status_code == 402:
                print e.description
            elif e.status_code == 409:
                print e.description
        
        return card
    
    def addClient(self, email, cardUri):
        try:
            client = balanced.Marketplace.my_marketplace.create_buyer(email, cardUri)
            
            return True
        except balanced.exc.HttpError as e:
            if e.category_code == "duplicate-email-address":
                buyer = balanced.Account.query.filter(email_address=email)
                print buyer
                buyer = buyer[0]
                buyer.add_card(cardUri)
            else:
                print e
        
        return False
    
    def register_buyer(self):
        name = raw_input("Name on card: ")
        email = raw_input("E-mail address: ")
        addr = raw_input("Street Address: ")
        city = raw_input("City: ")
        zip = raw_input("Zip Code: ")
        country = raw_input("2-digit Country Code: ")
        phone = raw_input("Phone Number: ")
        cc = raw_input("Credit Card #: ")
        month = raw_input("Month expiration: ")
        year = raw_input("Year expiration: ")
        cvv = raw_input("CVV2 #: ")
        
        card = self.addCC(name, cc, month, year, cvv)
        
        if not card:
            sys.exit("Unable to create card.")
        
        buyer = self.addClient(email, card.uri)
        
        if not buyer:
            sys.exit("Unable to create user in system.")
        
        return "%s has been registered to %s" % (cc, name)
    
    def charge(self, email, amount):
        if str(amount).find(".") != -1:
            amount = int(str(amount).replace(".", ""))
        else:
            amount = int(amount) * 100
        print "amount =", amount
        buyer = balanced.Account.query.filter(email_address=email)[0]
        return buyer.debit(amount=amount, appears_on_statement_as=self.getmarketplace())
    
    def getkey(self):
        return self.key
    
    def getmerchant(self):
        return balanced.Merchant.me.name
    
    def getmarketplace(self):
        return format(balanced.Marketplace.my_marketplace.name)
    
    def getescrow(self):
        return balanced.Marketplace.my_marketplace.in_escrow
    
    def search_email(self, crit):
        info = None
        
        try:
            info = balanced.Account.query.filter(email_address=crit)[0]
        except:
            pass
        
        return info
    
    def search_cc(self, cc):
        if not isinstance(cc, str):
            print "%d is not a string.  Converting." % (cc)
            cc = str(cc)
            print "cc =", cc
            
        if len(cc) > 4:
            cc = cc[-4:]
            print "Fetched last 4:", cc
        elif len(cc) < 4:
            print "Invalid length for CC"
            return False
        
        try:
            cards = list(balanced.Marketplace.query.one().cards)
            
            for card in cards:
                if card.last_four == cc:
                    return card
        except:
            pass
        
        return None
    
    def cc_valid(self, cc):
        info = self.search_cc(cc)
        
        if info:
            now = datetime.datetime.now()
            
            if info.expiration_year <= now.year:
                if info.expiration_month < now.month:
                    return [-1, "Expiration month has past."]
                
                if info.expiration_year < now.year:
                    return [-2, "Expiration year has past."]
                
            return [1, info]
        return [-3, "No record of %s was found in system." % (cc)]
    
if __name__ == "__main__":
    sfu = Balance()
    
    cc4 = raw_input("Last 4 of CC: ")
    
    code,val = sfu.cc_valid(cc4)
    
    if code == -3:
        print "No credit card found with given information."
        status = sfu.register_buyer()
        sys.exit(status)
    elif code != 1:
        sys.exit("Credit card is not valid: %d [%s]" % (code, val))
    else:
        owner = sfu.search_email(val.account.email_address)
        
        print "\nOwner Information:"
        print "-------------------"
        print "E-mail:", owner.email_address
        print "Role(s):", owner.roles
        print "ID:", owner.id
        print "Created:", owner.created_at
        
        print "\nCard Information:"
        print "-------------------"
        print "Expiration: %d/%d" % (val.expiration_month, val.expiration_year)
        print "Name on Card:", val.name
        print "Entered Into System:", val.created_at
        print "Brand:", val.brand
        print "Type:", val.card_type
        print "Last 4:", val.last_four
    
    print "\n\nCharge:"
    print "------------"
    charge = raw_input("How much to charge card: ")
    ret = sfu.charge(owner.email_address, charge)
    print "Fee:", ret.fee
    print "Amount charged:", ret.amount
    print "Created:", ret.created_at
    print "Available At:", ret.available_at
    print "Transaction ID:", ret.transaction_number
    print "Record ID:", ret.id