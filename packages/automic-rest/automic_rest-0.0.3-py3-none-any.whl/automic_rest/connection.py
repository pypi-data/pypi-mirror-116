import os 
from urllib.parse import urlparse

_userid = None
_password = None
_url = None
_sslverify = None 

class connection(object): 
    def __init__(self, **kwargs): 
        self.userid = kwargs.get('userid','') 
        self.password = kwargs.get('password','') 
        self.system = kwargs.get('system','').lower() 
        self.baseurl = kwargs.get('url','')
        self.noproxy = kwargs.get('noproxy',False)
        self.sslverify = kwargs.get('sslverify',True)
        
        self.domain = urlparse(self.baseurl).netloc 
        self.basepath = '/api/v1'
        self.url = self.baseurl+'/ae'+self.basepath 
        if self.noproxy: 
            os.environ['NO_PROXY'] = self.domain 
        
        self.init() 
 
    def init(self): 
        global _userid, _password, _url, _sslverify 
        _userid = self.userid 
        _password = self.password 
        _url = self.url 
        _sslverify = self.sslverify
 
class config(object): 
    def __init__(self): 
        self.url = _url 
        self.userid = _userid 
        self.password = _password 
        self.sslverify = _sslverify

    def setArgs(self, path, **kwargs):
        for key, value in kwargs.items():
            path = path.replace('{'+key+'}', str(value))
        return path

