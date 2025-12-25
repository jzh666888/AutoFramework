import unittest

from business.buRequests import get
from business.dataClear import clear_notes
from business.dataCreate import create_notes
from common.caseLog import class_case_decoration, info, case
from common.outputCheck import json_output_check
from common.yamlloader import env_config


@class_case_decoration
class GetNotesHandle(unittest.TestCase):
    host = env_config()['host']
    user_id = env_config()['userId']
    sid = env_config()['wps_sid']

    def setUp(self) -> None:
        #清除账号测试数据
        clear_notes(self.user_id, self.sid)

    def testCase01_getZeroData(self):
        """请求获取首页便签接口，测试获取0条数据"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求首页便签接口】')
        # 请求首页便签列表接口主流程步骤
        url = f'/v3/notesvr/user/1122610847/home/startindex/0/rows/0/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMessage': ''
        }
        self.assertEqual(400, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())

    def testCase02_getThreeData(self):
        """请求获取首页便签接口，测试获取3条数据"""
        info('【前置条件】新增3条便签数据')
        # 前置构建三条便签数据
        notes = create_notes(self.user_id, self.sid, 3)
        for note in notes:
            info(f'前置构建的3条便签数据:{note}')

        case('【请求首页便签接口】')
        # 请求首页便签列表接口主流程步骤
        url = f'/v3/notesvr/user/1122610847/home/startindex/0/rows/3/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'responseTime': int,
            'webNotes': [
                {
                    'noteId': notes[2]['noteId'],
                    'createTime': int,
                    'star': 0,
                    'remindTime': int,
                    'remindType': 0,
                    'infoVersion': 1,
                    'infoUpdateTime': int,
                    'groupId': None,
                    'title': 'test',
                    'summary': 'test',
                    'thumbnail': None,
                    'contentVersion': 1,
                    'contentUpdateTime': int
                },
                {
                    'noteId': notes[1]['noteId'],
                    'createTime': int,
                    'star': 0,
                    'remindTime': int,
                    'remindType': 0,
                    'infoVersion': 1,
                    'infoUpdateTime': int,
                    'groupId': None,
                    'title': 'test',
                    'summary': 'test',
                    'thumbnail': None,
                    'contentVersion': 1,
                    'contentUpdateTime': int
                },
                {
                    'noteId': notes[0]['noteId'],
                    'createTime': int,
                    'star': 0,
                    'remindTime': int,
                    'remindType': 0,
                    'infoVersion': 1,
                    'infoUpdateTime': int,
                    'groupId': None,
                    'title': 'test',
                    'summary': 'test',
                    'thumbnail': None,
                    'contentVersion': 1,
                    'contentUpdateTime': int
                }
            ]
        }
        self.assertEqual(200, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())

    def testCase03_permissionRestrictions(self):
        """请求获取首页便签接口，用其他用户获取当前用户所创建的便签内容(接口越权)"""
        info('【前置条件】当前用户新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        #用户B的user_id
        userIDB = 1123710849

        url = f'/v3/notesvr/user/{userIDB}/home/startindex/0/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            "errorCode": -1011,
            "errorMsg": "user change!"
        }
        self.assertEqual(412, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        json_output_check(expect_res, res.json())