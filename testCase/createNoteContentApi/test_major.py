import unittest

from business.buRequests import post
from business.dataClear import clear_notes
from business.dataCreate import create_notes, create_noteInfo
from common.caseLog import class_case_decoration, info, case
from common.outputCheck import json_output_check
from common.yamlloader import env_config


@class_case_decoration
class CreateNoteContent(unittest.TestCase):
    host = env_config()['host']
    user_id = env_config()['userId']
    sid = env_config()['wps_sid']
    url = '/v3/notesvr/set/notecontent'

    def setUp(self) -> None:
        # 清除账号测试便签数据
        clear_notes(self.user_id, self.sid)

    def testCase_major(self):
        """测试请求上传便签内容接口主流程"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口主流程步骤
        case('【请求上传便签内容接口步骤】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            'responseTime': int,
            'contentVersion': 1,
            'contentUpdateTime': int
        }
        self.assertEqual(200, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())
