
import uuid
import requests

from common.caseLog import case_decoration
from common.caseLog import info, error

# @case_decoration
def create_notes(user_id, sid, num, groupId=None, remindTime=0, delete=False, clear=False):
    info(f'【前置】构建{num}条便签数据')
    url_info = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'
    url_content = 'http://note-api.wps.cn' + '/v3/notesvr/set/notecontent'
    url_delete = 'http://note-api.wps.cn' + '/v3/notesvr/delete'
    headers = {
        'Content-Type': 'application/json',
        'X-User-Key': str(user_id),
        'Cookie': f'wps_sid={sid};'
    }
    result = []
    for i in range(num):
        note_id = str(uuid.uuid4()).replace('-', '')
        info_body = {"noteId": note_id, "star": 0}
        if groupId:
            # 构建分组便签
            info_body['groupId'] = groupId
        if remindTime != 0:
            info_body['remindTime'] = remindTime
            info_body['remindType'] = 1
        res = requests.post(url_info, headers=headers, json=info_body)
        if res.status_code != 200:
            raise ValueError(f'前置构建数据异常，状态码为{res.status_code}')
        content_body = {"noteId": note_id,
                        "title": "test",
                        "summary": "test",
                        "body": "test",
                        "localContentVersion": 1,
                        "BodyType": 0}
        res = requests.post(url_content, headers=headers, json=content_body)
        if res.status_code != 200:
            raise ValueError(f'前置构建数据异常，状态码为{res.status_code}')
        if delete or clear:
            body = {
                'noteId': note_id
            }
            res = requests.post(url_delete, headers=headers, json=body)
            if res != 200:
                raise ValueError(f'前置构建数据异常，状态码为{res.status_code}')
            if clear:
                pass
        note_res = {}
        for k, v in info_body.items():
            note_res[k] = v
        for k, v in content_body.items():
            note_res[k] = v
        result.append(note_res)
    return result

# @case_decoration
def create_noteInfo(user_id, sid, groupId=None, remindTime=0,star=None):
    info(f'【前置】构建便签主体')
    url_info = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'
    headers = {
        'Content-Type': 'application/json',
        'X-User-Key': str(user_id),
        'Cookie': f'wps_sid={sid};'
    }
    note_id = str(uuid.uuid4()).replace('-', '')
    info_body = {"noteId": note_id, "star": 0}
    if star:
        info_body['star'] = 1
    if groupId:
        # 构建分组便签
        info_body['groupId'] = groupId
    if remindTime != 0:
        info_body['remindTime'] = remindTime
        info_body['remindType'] = 1
    res = requests.post(url_info, headers=headers, json=info_body)
    info(f'便签主体响应response body:{res.text}')
    if res.status_code != 200:
        raise ValueError('构建便签主体失败')
    return note_id

def create_groups(user_id, sid, num, have_note=False):
    print(f'【前置】构建{num}条分组数据')
    result = []
    url = 'http://note-api.wps.cn' + '/v3/notesvr/set/notegroup'
    method = 'post'
    headers = {
        'Content-Type': 'application/json',
        'X-User-Key': str(user_id),
        'Cookie': f'wps_sid={sid};'
    }
    for i in range(num):
        group_id = str(uuid.uuid4()).replace('-', '')
        group_name = 'test' + f'{i}'
        order = 0
        body = {"groupId": group_id, "groupName": group_name, "order": order}

        res = requests.request(method=method, url=url, headers=headers, json=body)
        if res.status_code != 200:
            raise ValueError('【dataCreate】http error')
        if have_note:
            # 实现分组便签数据新增操作
            pass
        result.append(body)
    return result