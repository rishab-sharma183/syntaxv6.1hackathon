# Syntax V6.1 Submission by Rishab Sharma and Hanif Patel

## All code copied is listed below

- For the frontend, Bootstrap was used


- https://esd.io/blog/flask-apps-heroku-real-ip-spoofing.html  
  This code is a "Safer" fix for being able to access a user's remote address

```python
class SaferProxyFix(object):
    """This middleware can be applied to add HTTP proxy support to an
    application that was not designed with HTTP proxies in mind.  It
    sets `REMOTE_ADDR`, `HTTP_HOST` from `X-Forwarded` headers.
    
    If you have more than one proxy server in front of your app, set
    num_proxy_servers accordingly
    Do not use this middleware in non-proxy setups for security reasons.
    
    get_remote_addr will raise an exception if it sees a request that 
    does not seem to have enough proxy servers behind it so long as
    detect_misconfiguration is True.
    The original values of `REMOTE_ADDR` and `HTTP_HOST` are stored in
    the WSGI environment as `werkzeug.proxy_fix.orig_remote_addr` and
    `werkzeug.proxy_fix.orig_http_host`.
    :param app: the WSGI application
    """

    def __init__(self, app, num_proxy_servers=1, detect_misconfiguration=False):
        self.app = app
        self.num_proxy_servers = num_proxy_servers
        self.detect_misconfiguration = detect_misconfiguration

    def get_remote_addr(self, forwarded_for):
        """Selects the new remote addr from the given list of ips in
        X-Forwarded-For.  By default the last one is picked. Specify
        num_proxy_servers=2 to pick the second to last one, and so on.
        """
        if self.detect_misconfiguration and not forwarded_for:
            raise Exception(
                "SaferProxyFix did not detect a proxy server. Do not use this fixer if you are not behind a proxy.")
        if self.detect_misconfiguration and len(forwarded_for) < self.num_proxy_servers:
            raise Exception("SaferProxyFix did not detect enough proxy servers. Check your num_proxy_servers setting.")

        if forwarded_for and len(forwarded_for) >= self.num_proxy_servers:
            return forwarded_for[-1 * self.num_proxy_servers]

    def __call__(self, environ, start_response):
        getter = environ.get
        forwarded_proto = getter('HTTP_X_FORWARDED_PROTO', '')
        forwarded_for = getter('HTTP_X_FORWARDED_FOR', '').split(',')
        forwarded_host = getter('HTTP_X_FORWARDED_HOST', '')
        environ.update({
            'werkzeug.proxy_fix.orig_wsgi_url_scheme': getter('wsgi.url_scheme'),
            'werkzeug.proxy_fix.orig_remote_addr': getter('REMOTE_ADDR'),
            'werkzeug.proxy_fix.orig_http_host': getter('HTTP_HOST')
        })
        forwarded_for = [x for x in [x.strip() for x in forwarded_for] if x]
        remote_addr = self.get_remote_addr(forwarded_for)
        if remote_addr is not None:
            environ['REMOTE_ADDR'] = remote_addr
        if forwarded_host:
            environ['HTTP_HOST'] = forwarded_host
        if forwarded_proto:
            environ['wsgi.url_scheme'] = forwarded_proto
        return self.app(environ, start_response)
```

- If you wanted me to include it, I copied a bit of code from RapidApi but it's just a few lines of code which are for
  requesting the weather API being used

```python
import requests

url = "https://weatherapi-com.p.rapidapi.com/forecast.json"

querystring = {"q": "Patna", "days": "3"}

headers = {
    "X-RapidAPI-Key": "e7c36d5797mshd71062d4e8e481fp14e867jsn504cabd7da67",
    "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring).json()

print(response)
```

## How it was made

I, Rishab Sharma and my partner, Hanif Patel are the creators of this small website which is able to show the future
weather of 3 days and the current weather. The website uses
an [API listed on RapidApi](https://rapidapi.com/weatherapi/api/weatherapi-com/)
which we have the free plan of. The free plan granted us 1,000,000 uses per month with 3 day future forecasts and
realtime forecasts. We thought this was a great deal and moved on with using it. The website uses geocoder, a python
package, to find the city you are in using your IP address. After finding it, it submits the city to 2 endpoints of the
api, one that gets future forecasts and another that gets realtime weather. After requesting the endpoint with the
parameters, it gets all the relevant data from the response and formats it into a dictionary which is then transferred
to the front-end or the client side. The client side then uses Jinja2 (which is sort of like python but in html) to
place all the information given by the backend in its relevant spots. It also uses the suitable default icon given to
us by the API.

### Features

- The website gives the future forcast for 3 days.
- It gives the real-time weather including whether it is daytime or nighttime.
- It automatically gets your location securely.
- You are able to select any other city you want to see the weather of.

### What we couldn't accomplish

- We weren't able to get images of the locations due to the lack of time and the changes in submission dates.
- The website's design is incredibly simple, again because of a lack of time. We weren't able to create a proper design.
- We weren't able to get a greater number of days for the future forecast because we are making this project without any expenses.
 
# To access the main website, go to the link below
## https://hackathondps.pythonmage.repl.co

### Thank you for visiting,
#### Regards, Rishab Sharma and Hanif Patel of Boston World School