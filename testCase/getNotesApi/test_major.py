import unittest

import requests

from business.buRequests import get
from business.dataClear import clear_notes
from business.dataCreate import create_notes
from common.caseLog import class_case_decoration, case, info
from common.outputCheck import json_output_check
from common.yamlloader import env_config


@class_case_decoration
class GetNotes(unittest.TestCase):
    host = env_config()['host']
    user_id = env_config()['userId']
    sid = env_config()['wps_sid']
    url = f'/v3/notesvr/user/{user_id}/home/startindex/0/rows/1/notes'

    def setUp(self) -> None:
        #清除账号测试数据
        clear_notes(self.user_id, self.sid)

    def testCase_major(self):
        """测试请求首页便签列表接口主流程"""
        # info('【前置条件】新增一条便签数据')
        #前置构建一条便签数据
        notes = create_notes(self.user_id,self.sid,1)
        info(f'前置构建的一条便签数据:{notes[0]}')
        case('【请求首页便签接口】')

        #请求首页便签列表接口主流程步骤
        url = self.host + self.url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=url, body=None, headers=headers)
        expect_res = {
            'responseTime':int,
            'webNotes':[
                {
                    'noteId':notes[0]['noteId'],
                    'createTime': int,
                    'star': 0,
                    'remindTime': int,
                    'remindType': 0,
                    'infoVersion': 1,
                    'infoUpdateTime':int,
                    'groupId': None,
                    'title': 'test',
                    'summary': 'test',
                    'thumbnail': None,
                    'contentVersion': 1,
                    'contentUpdateTime': int
                }
            ]
        }
        self.assertEqual(200,res.status_code,msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())




