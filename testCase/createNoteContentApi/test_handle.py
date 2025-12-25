import unittest

from business.buRequests import post, get
from business.dataClear import clear_notes, clear_groups
from business.dataCreate import create_noteInfo, create_groups
from common.caseLog import class_case_decoration, info, case
from common.outputCheck import json_output_check
from common.yamlloader import env_config


@class_case_decoration
class CreateNoteContentHandle(unittest.TestCase):
    host = env_config()['host']
    user_id = env_config()['userId']
    sid = env_config()['wps_sid']
    url = '/v3/notesvr/set/notecontent'
    group_url = '/v3/notesvr/web/getnotes/group'

    def setUp(self) -> None:
        # 清除便签数据
        clear_notes(self.user_id, self.sid)
        #删除分组
        clear_groups(self.user_id, self.sid)

    def testCase01_updateNoteContent(self):
        """请求上传便签内容接口,测试能否正常更新便签内容"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口，新增便签数据
        case('【请求上传便签内容】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res1 = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        self.assertEqual(200, res1.status_code, msg=f'状态码断言失败，response text{res1.text}')
        expect_res1 = {
            'responseTime': int,
            'contentVersion': 1,
            'contentUpdateTime': int
        }
        json_output_check(expect_res1, res1.json())

        # 再次请求上传便签内容接口，更新新增的便签内容
        case('【更新便签内容】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test2',
            'summary': 'test2',
            'body': 'test2',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res2 = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res2 = {
            'responseTime': int,
            'contentVersion': 2,
            'contentUpdateTime': int
        }
        self.assertEqual(200, res2.status_code, msg=f'状态码断言失败，response text{res2.text}')
        json_output_check(expect_res2, res2.json())

    def testCase02_error_updateNoteContent(self):
        """请求上传便签内容接口,测试更新便签内容时输入错误的版本号"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口，新增便签数据
        case('【请求上传便签内容】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res1 = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res1 = {
            'responseTime': int,
            'contentVersion': 1,
            'contentUpdateTime': int
        }
        json_output_check(expect_res1, res1.json())

        # 再次请求上传便签内容接口，更新新增的便签内容，输入错误的localContentVersion版本号
        case('【更新便签内容】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 2,
            'BodyType': 0
        }
        res2 = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            'errorCode': -1003,
            'errorMsg': 'content version not equal!'
        }
        self.assertEqual(412, res2.status_code, msg=f'状态码断言失败，response text{res2.text}')
        json_output_check(expect_res, res2.json())

    def testCase03_notFountNoteId_updateNoteContent(self):
        """请求上传便签内容接口,测试更新便签内容时输入不存在的noteId"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口，新增便签数据
        case('【请求上传便签内容】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        expect_res = {
            "responseTime": int,
            "contentVersion": 1,
            "contentUpdateTime": int
        }
        res1 = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        self.assertEqual(200, res1.status_code, msg=f'状态码断言失败，response text{res1.text}')
        json_output_check(expect_res, res1.json())

        # 再次请求上传便签内容接口，更新新增的便签内容，输入主体不存在的noteId
        case('【更新便签内容】')
        req_url = self.host + self.url
        req_body = {
            'noteId': '1111111111',
            'title': 'test2',
            'summary': 'test2',
            'body': 'test2',
            'localContentVersion': 2,
            'BodyType': 0
        }
        res2 = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res2 = {
            'errorCode': -1002,
            'errorMsg': 'Note Not Exist!'
        }
        self.assertEqual(412, res2.status_code, msg=f'状态码断言失败，response text{res2.text}')
        json_output_check(expect_res2, res2.json())

    def testCase04_permissionRestrictions(self):
        """请求上传便签内容接口,用其他用户获取当前用户所创建的便签内容(接口越权)"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口，用用户B的userId和sid新增便签数据
        case('【请求上传便签内容】')
        req_url = self.host + self.url

        # 用户B的user_id
        userIDB = 1123710849
        # 用户B的sid
        wps_sidB = 'V02SH23fI8M5bC4ctXMykm6gne53xYo00a7332920042e9ae8e;'
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = post(user_id=userIDB, sid=wps_sidB, url=req_url, body=req_body)
        expect_res = {
            'errorCode': -1002,
            'errorMsg': 'Note Not Exist!'
        }
        self.assertEqual(401, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())

    def testCase05_error_localContentVersion(self):
        """请求上传便签内容接口,测试上传便签内容的请求参数localContentVersion输入0的情况"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口
        case('【请求上传便签内容接口】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 0,
            'BodyType': 0
        }
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            'errorCode': -2009,
            'errorMsg': ''
        }
        self.assertEqual(400, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())

    def testCase06_error_bodyType(self):
        """请求上传便签内容接口,测试上传便签内容的请求参数BodyType输入-1的情况"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        # 请求上传便签内容接口
        case('【请求上传便签内容接口】')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': -1
        }
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            'errorCode': -2009,
            'errorMsg': ''
        }
        self.assertEqual(400, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())

    def testCase07_createGroupNote(self):
        """请求上传便签内容接口,测试上传分组便签数据"""
        info('【前置条件】新增一条分组数据')
        group_data = create_groups(user_id=self.user_id, sid=self.sid, num=1, have_note=False)
        group_id = group_data[0]['groupId']
        info(f'前置构建的分组便签主体数据返回的便签id:{group_id}')

        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid, groupId=group_id, star=1)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        ## 请求上传便签内容接口
        case('【请求上传便签内容接口】')
        req_url = self.host + self.url
        req_body1 = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        expect_res = {
            'responseTime': int,
            'contentVersion': 1,
            'contentUpdateTime': int
        }
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body1)
        self.assertEqual(200, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res, res.json())

        #请求首页便签接口
        req_url2 = self.host + f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/1/notes'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res2 = get(user_id=self.user_id, sid=self.sid, url=req_url2, body=None, headers=headers)
        expect_res2 = {
            'responseTime': int,
            'webNotes': []
        }
        self.assertEqual(200, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res2, res2.json())

        #查看分组下的便签数据
        req_url3 = self.host + self.group_url
        req_body3 = {
            'groupId':group_id,
            'startIndex':0,
            'rows':10
        }
        res3 = post(user_id=self.user_id, sid=self.sid, url=req_url3, body=req_body3)
        expect_res3 = {
            'responseTime': int,
            'webNotes': [
                {
                    'noteId':noteId,
                    'createTime':int,
                    'star':1,
                    'remindTime':int,
                    'remindType':0,
                    'infoVersion': 1,
                    'infoUpdateTime': int,
                    'groupId': group_id,
                    'title': 'test',
                    'summary': 'test',
                    'thumbnail': None,
                    'contentVersion': 1,
                    'contentUpdateTime': int

                }
            ]
        }
        self.assertEqual(200, res.status_code, msg=f'状态码断言失败，response text{res.text}')
        json_output_check(expect_res3, res3.json())

