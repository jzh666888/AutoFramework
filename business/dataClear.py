import requests



def clear_groups(user_id, sid):
    url = 'http://note-api.wps.cn' + '/v3/notesvr/get/notegroup'
    method = 'post'
    headers = {
        'Content-Type': 'application/json',
        'X-User-Key': str(user_id),
        'Cookie': f'wps_sid={str(sid)};'
    }

    body = {"excludeInValid": True}
    res = requests.request(method=method, url=url, headers=headers, json=body)
    if res.status_code != 200:
        raise ValueError('【dataClear】http get notegroup error')
    group_ids = []
    for group in res.json()['noteGroups']:
        group_ids.append(group['groupId'])

    url = 'https://note-api.wps.cn/notesvr/delete/notegroup'
    headers = {
        'Content-Type': 'application/json',
        'X-User-Key': str(user_id),
        'Cookie': f'wps_sid={sid};'
    }
    for group_id in group_ids:
        body = {
            'groupId': group_id
        }
        res = requests.post(url, headers=headers, json=body)
        if res.status_code != 200:
            raise ValueError('【dataClear】http delete group error')

def clear_notes(user_id, sid):
    info_url = f'http://note-api.wps.cn/v3/notesvr/user/{user_id}/home/startindex/0/rows/100/notes'
    delete_url = 'http://note-api.wps.cn' + '/v3/notesvr/delete'
    deleteHsz_url = 'http://note-api.wps.cn' '/v3/notesvr/cleanrecyclebin'
    info_method = 'get'
    delete_method = 'post'
    deleteHsz_method = 'post'
    info_headers = {
        'Content-Type': 'application/json',
        'Cookie': f'wps_sid={str(sid)};'
    }

    delete_headers = {
        'Content-Type': 'application/json',
        'X-User-Key': str(user_id),
        'Cookie': f'wps_sid={sid};'
    }

    res = requests.request(method=info_method, url=info_url, headers=info_headers)
    note_id = []
    for note in res.json()['webNotes']:
        note_id.append(note['noteId'])
    for noteId in note_id:
        body = {
            'noteId':noteId
        }
        res = requests.request(method=delete_method, url=delete_url, headers=delete_headers, json=body)
        if res.status_code != 200:
            raise ValueError('便签删除失败')

    """标签清空回收站"""
    hsz_body = {
        'noteIds':[-1]
    }
    res = requests.request(method=deleteHsz_method, url=deleteHsz_url, headers=delete_headers, json=hsz_body)
    if res.status_code != 200:
        raise ValueError('清空回收站失败')

