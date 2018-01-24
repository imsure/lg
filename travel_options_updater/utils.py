import requests

def query_parade():
    url = 'http://TUCParadeELB-1716058470.us-west-2.elb.amazonaws.com/sp'
    # url = 'http://54.218.80.167:8103/sp'
    params = {
        "start_lat": 32.07845,
        "start_lon": -110.62901,
        "end_lat": 32.53766,
        "end_lon": -110.94301,
        "departure_time": "12:45",
        "toll": "true"
    }
    r = requests.post(url, json=params)
    print(r.text)
    print(r.status_code)
