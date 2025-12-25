import requests

from common.caseLog import info, error


def post(user_id,sid,url,body,headers=None):
    if not headers:
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(user_id),
            'Content-Type': 'application/json'
        }
    info(f'request url: {url}')
    info(f'request headers: {headers}')
    info(f'request body: {body}')
    try:
        res = requests.post(url, headers=headers, json=body, timeout=5)
    except TimeoutError:
        error(f'url: {url}, requests timeout！')
        return 'Requests Timeout!'
    info(f'response code: {res.status_code}')
    info(f'response body: {res.text}')
    return res

def get(user_id,sid,url,body,headers=None):
    if not headers:
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(user_id),
            'Content-Type': 'application/json'
        }
    info(f'request url: {url}')
    info(f'request headers: {headers}')
    info(f'request body: {body}')
    try:
        if body == None:
            res = requests.get(url, headers=headers, timeout=5)
        else:
            res = requests.get(url, headers=headers, json=body, timeout=5)
    except TimeoutError:
        error(f'url: {url}, requests timeout！')
        return 'Requests Timeout!'
    info(f'response code: {res.status_code}')
    info(f'response body: {res.text}')
    return res