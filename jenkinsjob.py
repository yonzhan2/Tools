import urllib.parse
import requests


def build_jenkins_job(url, username, password):
    """Post to the specified Jenkins URL.

    `username` is a valid user, and `password` is the user's password or
    (preferably) hex API token.
    """
    # Build the Jenkins crumb issuer URL
    parsed_url = urllib.parse.urlparse(url)
    crumb_issuer_url = urllib.parse.urlunparse((parsed_url.scheme,
                                                parsed_url.netloc,
                                                'crumbIssuer/api/json',
                                                '', '', ''))

    # Get the Jenkins crumb
    auth = requests.auth.HTTPBasicAuth(username, password)
    r = requests.get(crumb_issuer_url, auth=auth)
    json = r.json()
    crumb = {json['crumbRequestField']: json['crumb']}

    # POST to the specified URL
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    headers.update(crumb)
    r = requests.post(url, headers=headers, auth=auth)


username = 'admin'
password = 'pass'
url = 'http://10.224.38.201:8080/job/deployfrontend4msjun/build'
build_jenkins_job(url, username, password)
