# -------------------#
import urllib2
import urllib
import json

__name__ = "sqtest_sqdemo27u02"
__password__ = "P@ss1234"


def postHttp(url=None, values=None, headers=None):
    request = urllib2.Request(url, values, headers)
    ret = None
    response = None
    try:
        response = urllib2.urlopen(request)
        ret = str(response.getcode())
    # print ret
    except urllib2.HTTPError, e:
        ret = str(e)
        response = e.read()
    except urllib2.URLError, e:
        ret = e.reason
        response = ''
    finally:
        return ret, response


# get token -------------------------------------------------------
url = "https://idbroker.webex.com/idb/oauth2/v1/access_token"
values = "grant_type=client_credentials&client_id=Cd6966e933eea56cb9fc3dabfd3d7dd51dc9594ce857bc81f173eae82da8348be&client_secret=4fc884b0c4695b515cb117719ef48e1fd988f2973e59810a70ea7c0c136a47f5&scope=webexsquare:get_conversation Identity:SCIM spark:kms"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
ret = 'Failed'
ret, response = postHttp(url, values, headers)
if (ret == '200'):
    BearToken = json.loads(response.read())
    if BearToken['token_type'] == 'Bearer':
        bearToken = BearToken['access_token']
    else:
        print 'token type Bearer NOT found!'
        exit()
else:
    print 'Failed to get token, reason:' + str(ret) + '\r\n' + response
    exit()

# print bearToken

# set account ------------------------------------------------------
url = "https://conv-a.wbx2.com/conversation/api/v1/users/test_users_s"
headers = {'Content-Type': 'application/json'}
headers['Authorization'] = "Bearer " + bearToken.encode("ascii")
# print headers

values = {"emailTemplate": __name__ + "@squared.example.com", "password": __password__, "displayName": __name__,
          "entitlements": ["webExSquared", "squaredTeamMember", "spark"]}
# print Account
data = json.dumps(values)
# print values
ret, response = postHttp(url, data, headers)
if (ret == '200'):
    print "OK, account refreshed!\r\n" + "name:" + values['emailTemplate'] + "\r\npassword:" + values['password']
else:
    print "Failed, account not refreshed! reason:" + str(ret) + "\r\n" + response
# print ret
