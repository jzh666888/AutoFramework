import unittest

from parameterized import parameterized

from business.buRequests import post
from business.dataClear import clear_notes
from business.dataCreate import create_noteInfo
from common.caseLog import class_case_decoration, info, case
from common.outputCheck import json_output_check
from common.yamlloader import env_config


@class_case_decoration
class CreateNoteContentCaseInput(unittest.TestCase):
    host = env_config()['host']
    user_id = env_config()['userId']
    url = '/v3/notesvr/set/notecontent'
    sid = env_config()['wps_sid']
    # 已被淘汰的身份信息
    endSid = 'V02S2Q82jHN0RiLA99F1fdMWV_1xmMw00ad1757d0042e9ae9f;'
    must_key = (
        ['noteId', 500], ['title', 200], ['summary', 200], ['body', 412], ['localContentVersion', 200],
        ['BodyType', 200])

    def setUp(self) -> None:
        """前置清除测试数据"""
        clear_notes(self.user_id, self.sid)

    @parameterized.expand(must_key)
    def testCase01_remove_must_key(self, key, code):
        """测试请求上传便签内容接口的必填项缺失校验"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case01:必填项{key}缺少校验')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        req_body.pop(key)
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        self.assertEqual(code, res.status_code, msg=f'状态码断言失败， response text: {res.text}')

    @parameterized.expand(must_key)
    def testCase02_null_must_key(self, key, code):
        """测试请求上传便签内容接口的必填项的值为null"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case03:必填项{key}值为null')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        req_body[key] = None
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        self.assertEqual(code, res.status_code, msg=f'状态码断言失败， response text: {res.text}')

    @parameterized.expand(must_key)
    def testCase03_valueEmptyString_must_key(self, key, code):
        """测试请求上传便签内容接口的必填项的值为空字符串"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case03:必填项{key}值为""')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        req_body[key] = ""
        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body)
        self.assertEqual(code, res.status_code, msg=f'状态码断言失败， response text: {res.text}')

    def testCase04_removeKey_xUserKey_must_key(self):
        """测试请求上传便签内容接口的请求头X-User-Key的字段缺失"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case04:X-Key-User字段缺失""')
        req_url = self.host + self.url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body, headers=headers)
        self.assertEqual(412, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        expect_res = {
            'errorCode': -1011,
            'errorMsg': 'X-user-key header Requested!'
        }
        json_output_check(expect_res, res.json())

    def testCase05_valueNull_xUserKey_must_key(self):
        """测试请求上传便签内容接口的请求头X-User-Key的字段值为null"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case05:X-Key-User字段的值为null')
        req_url = self.host + self.url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}',
            'X-user-key': None
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=None, sid=self.sid, url=req_url, body=req_body, headers=headers)
        self.assertEqual(412, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        expect_res = {
            'errorCode': -1011,
            'errorMsg': 'X-user-key header Requested!'
        }
        json_output_check(expect_res, res.json())

    def testCase06_valueEmpty_xUserKey_must_key(self):
        """测试请求上传便签内容接口的请求头X-User-Key的字段值为空字符串"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case06:X-Key-User字段的值为""')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id="", sid=self.sid, url=req_url, body=req_body)
        self.assertEqual(412, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        expect_res = {
            'errorCode': -1011,
            'errorMsg': 'X-user-key header Requested!'
        }
        json_output_check(expect_res, res.json())

    def testCase07_boundary_xUserKey(self):
        """测试请求上传便签内容接口的请求头X-User-Key的边界值"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case07:X-Key-User字段的值超出边界值')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        # 测试数据
        test_userId = 11226108471

        res = post(user_id=test_userId, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            'errorCode': -1011,
            'errorMsg': 'user change!'
        }
        self.assertEqual(412, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        json_output_check(expect_res, res.json())

    def testCase08_specialChar_xUserKey(self):
        """测试请求上传便签内容接口的请求头X-User-Key的值存在特殊标点字符"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case08:X-Key-User字段的值存在特殊标点字符')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        # 测试数据
        test_userId = '1122610847.'

        res = post(user_id=test_userId, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            "errorCode":-7,
            "errorMsg":"参数类型错误！"
        }
        self.assertEqual(500, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        json_output_check(expect_res, res.json())

    def testCase09_notEnum_xUserKey(self):
        """测试请求上传便签内容接口的请求头X-User-Key的值为非枚举值"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case09:X-Key-User字段的值为非枚举值')
        req_url = self.host + self.url
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        # 测试数据
        test_userId = 1111111111

        res = post(user_id=test_userId, sid=self.sid, url=req_url, body=req_body)
        expect_res = {
            'errorCode': -1011,
            'errorMsg': 'user change!'
        }
        self.assertEqual(412, res.status_code, msg=f'状态码断言失败， response text: {res.text}')
        json_output_check(expect_res, res.json())

    def testCase10_keyRemove_sid(self):
        """测试请求上传便签内容接口的请求头wps_sid的字段缺失"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case010:wps_sid的字段缺失')
        req_url = self.host + self.url

        headers = {
            'X-user-key': str(self.user_id),
            'Content-Type': 'application/json'
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body, headers=headers)
        expect_res = {
            'errorCode': -2009,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase11_valueKeyEmptyString_sid(self):
        """测试请求上传便签内容接口的请求头wps_sid的字段值为空字符串"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case011:wps_sid的字段值为空字符串')
        req_url = self.host + self.url

        headers = {
            'X-user-key': str(self.user_id),
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=""'
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body, headers=headers)
        expect_res = {
            'errorCode': -2009,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase12_valueNull_sid(self):
        """测试请求上传便签内容接口的请求头wps_sid的字段值为null"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case012:wps_sid的字段值为null')
        req_url = self.host + self.url

        headers = {
            'X-user-key': str(self.user_id),
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=null'
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase13_error_sid(self):
        """测试请求上传便签内容接口的请求头wps_sid的字段值为错误的sid"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case013:wps_sid的字段值为错误的sid')
        req_url = self.host + self.url

        headers = {
            'X-user-key': str(self.user_id),
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02S2Q82jHN0RiLA99F1fBBBB_1xmMw00ad1757d0042e9ae9f;'
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase14_end_sid(self):
        """测试请求上传便签内容接口的请求头wps_sid的字段值为过期的sid"""
        info('【前置条件】新增一条便签主体数据')
        # 前置构建一条便签数据，并返回noteId
        noteId = create_noteInfo(user_id=self.user_id, sid=self.sid)
        info(f'前置构建的便签主体数据返回的便签id:{noteId}')

        case(f'Case014:wps_sid的字段值为过期的sid')
        req_url = self.host + self.url

        headers = {
            'X-user-key': str(self.user_id),
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.endSid}'
        }
        req_body = {
            'noteId': noteId,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }

        res = post(user_id=self.user_id, sid=self.sid, url=req_url, body=req_body, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())