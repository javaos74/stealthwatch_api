# -*- coding: utf-8 -*-

import requests
import json
import pprint
import logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

SMC_HOST="10.72.80.171"
API_ENDPOINT = "https://10.72.80.171/smc"
API_HEADER = {"Content-Type": "application/json;charset=UTF-8", \
              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0", \
              "Referer": "https://10.72.80.171/lc-landing-page/", "Cookie":""} #, "Cookie": "JSESSIONID=475C7C3E5C29260C1E6AF431478D41D1; JSESSIONID=416C3BC0B4754464F322248B480F0D13"}

req = requests.Session()
#req.max_redirects = 2

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True

def login_via_web( user, pwd):
    _url = "{0}/j_spring_security_check".format( API_ENDPOINT)
    body = "j_username={0}&j_password={1}&submit=".format( user, pwd)
    resp = req.post( url=_url, headers={"Content-Type": "application/x-www-form-urlencoded", \
                                "Referer": "https://10.72.80.171/lc-landing-page/", \
                                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0",\
                                "Origin": "https://10.72.80.171"}, \
        allow_redirects=True, data=body, verify=False)
    if resp.status_code in[200, 302]:
        print(resp.status_code)
    vals = []
    if resp.cookies:
        for c in resp.cookies:
            vals.append("{0}={1}".format( c.name, c.value))
        API_HEADER['Cookie'] = ";".join(vals)
        return resp.cookies
    if req.cookies:
        for c in req.cookies:
            vals.append("{0}={1}".format( c.name, c.value))
        API_HEADER['Cookie'] = ";".join(vals)        
        return req.cookies

def login( user, pwd):
    _url = "{0}/{1}".format( API_ENDPOINT, user)
    resp = req.post( url=_url, headers={"Content-Type": "text/plain; charset=UTF-8"}, \
        allow_redirects=False, data=pwd, verify=False)
    if resp.status_code == 302:
        print(resp.status_code, resp.text)
    vals = []
    if resp.cookies:
        for c in resp.cookies:
            vals.append("{0}={1}".format( c.name, c.value))
        API_HEADER['Cookie'] = ";".join(vals)

    return resp.cookies

def get_api_simple( api_path, cookie):
    _url = "{0}/rest/{1}".format( API_ENDPOINT, api_path)
    resp = req.get( url=_url, headers=API_HEADER, allow_redirects=False, verify=False)
    #print(API_HEADER)
    if resp.status_code in [200,302]:
        try:
            pprint.pprint( json.loads(resp.text), indent=2)
        except ValueError as e:
            print( e)
            #print( "orignal response message\n{0}".format( resp.text))
    else:
        print(resp.status_code, resp.text)

def get_api_param( api_path, cookie, vals):
    _api_param = api_path.format(vals)
    _url = "{0}/rest{1}".format( API_ENDPOINT, _api_param)
    resp = req.get( url=_url, headers=API_HEADER, allow_redirects=False, verify=False)
    print(_url, API_HEADER)
    if resp.status_code in [200,302]:
        try:
            pprint.pprint( json.loads(resp.text), indent=2)
        except ValueError as e:
            print( e)
            #print( "orignal response message\n{0}".format( resp.text))
    else:
        print(resp.status_code, resp.text)

def list_domains( cookie ):
    return get_api_simple("/system/domains", cookie)

def list_hosts( cookie):
    return get_api_simple("/hostTraffic/list", cookie)

def get_last_traffic( cookie ):
    return get_api_simple("/hostTraffic/getLastFlowReceivedDateTime", cookie)

def get_api_info( cookie):
    return get_api_simple("/appliance/api/info", cookie)

if __name__ == '__main__':
    cookie = login_via_web('smc_api', '1234Qwer')
    api_names = ["/appliance/api/info", "/system/domains", "/product/info", "/ssotoken"]
    for api in api_names:
        print( "api {0} called ...".format(api))
        get_api_simple( api, cookie)
    get_api_param( '/domains/{0}/hostGroupIndex', cookie, "133" )    
    get_api_param( "/domains/{0}/hostgroups/dashboard", cookie, "133")

