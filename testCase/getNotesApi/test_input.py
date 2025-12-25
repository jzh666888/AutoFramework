import unittest

from business.buRequests import get
from business.dataClear import clear_notes
from business.dataCreate import create_notes
from common.caseLog import class_case_decoration, info, case
from common.outputCheck import json_output_check
from common.yamlloader import env_config


@class_case_decoration
class GetNotesCaseInput(unittest.TestCase):
    host = env_config()['host']
    user_id = env_config()['userId']
    sid = env_config()['wps_sid']
    #已被淘汰的身份信息
    endSid = 'V02S2Q82jHN0RiLA99F1fdMWV_1xmMw00ad1757d0042e9ae9f;'

    def setUp(self) -> None:
        """前置清除测试数据"""
        clear_notes(self.user_id, self.sid)

    def testCase01_null_userId(self):
        """测试请求首页便签接口,必填项userId为null"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/null/home/startindex/0/rows/10/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id,sid=self.sid,url=req_url,body=None,headers=headers)
        expect_res = {
            'errorCode':-7,
            'errorMsg':'参数类型错误！'
        }
        self.assertEqual(500,res.status_code)
        json_output_check(expect_res, res.json())

    def testCase02_null_startindex(self):
        """测试请求首页便签接口,必填项startindex为null"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/null/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -7,
            'errorMsg': '参数类型错误！'
        }
        self.assertEqual(500, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase03_null_rows(self):
        """测试请求首页便签接口,必填项rows为null"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/null/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -7,
            'errorMsg': '参数类型错误！'
        }
        self.assertEqual(500, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase04_boundary_startindex(self):
        """测试请求首页便签接口,必填项startindex为-1"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/-1/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.sid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -7,
            'errorMsg': '参数类型错误！'
        }
        self.assertEqual(200, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase05_keyRemove_sid(self):
        """测试请求首页便签接口,请求头必填项sid缺失"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -2009,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase06_valueKeyEmptyString_sid(self):
        """测试请求首页便签接口,请求头必填项sid的值为空字符串"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid='
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -2009,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase07_valueNull_sid(self):
        """测试请求首页便签接口,请求头必填项sid的值为null"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=null'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase08_error_sid(self):
        """测试请求首页便签接口,请求头必填项sid的值为错误的身份信息"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'wps_sid=V02S2Q82jHN0RiLA99F1fBBBB_1xmMw00ad1757d0042e9ae9f;'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())

    def testCase09_end_sid(self):
        """测试请求首页便签接口,请求头必填项sid的值为过期的身份信息"""
        info('【前置条件】新增一条便签数据')
        # 前置构建一条便签数据
        notes = create_notes(self.user_id, self.sid, 1)
        info(f'前置构建的一条便签数据:{notes[0]}')

        case('【请求获取首页便签接口】')
        url = f'/v3/notesvr/user/{self.user_id}/home/startindex/0/rows/1/notes'
        req_url = self.host + url
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={self.endSid}'
        }
        res = get(user_id=self.user_id, sid=self.sid, url=req_url, body=None, headers=headers)
        expect_res = {
            'errorCode': -2010,
            'errorMsg': ''
        }
        self.assertEqual(401, res.status_code)
        json_output_check(expect_res, res.json())