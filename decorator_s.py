from functools import wraps
import time
import requests


def check_cmc():
    cmcurl = 'csgcmc.qa.webex.com'
    try:
        res = requests.get(f"https://{cmcurl}/cmc/api/healthcheck/").json()
        ret = res['result']
    except Exception as e:
        # print(f"CMC {cmcurl} is not available due to {e}")
        ret = "NONONO"
    if ret == "OKOKOK":
        return True
    else:
        return False


def is_cmc_available(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("checking cmc ...")
        cmcurl = args[0]
        try:
            res = requests.get(f"https://{cmcurl}/cmc/api/healthcheck/").json()
            ret = res['result']
        except Exception as e:
            # print(f"CMC {cmcurl} is not available due to {e}")
            ret = "NONONO"
        if ret != "OKOKOK":
            print("cmc error")
        else:
            func(*args, **kwargs)

    return wrapper


@is_cmc_available
def test(cmculr, x):
    print(f"sleep1 {x}...")
    time.sleep(x)
    print("sleep2...")


test('csgcmc.qa.webex.com1', 3)
