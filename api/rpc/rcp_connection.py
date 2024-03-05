import xmlrpc.client

# CONF ==============>
url = "http://odoo:8069"
db = "gomaxtracker"
username = 'admin'
password = "004e331a922fb8f27aa72d8ff950730a42adb534"
# END ================>

def rpcConnection():
     common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
     return common.authenticate(db, username, password, {})          

def rcpModel():       
        return xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))      