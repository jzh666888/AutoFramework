import os
import sys
import unittest

from reportTool.BeautifulReport import BeautifulReport

DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    case_dir = './testCase'
    if len(sys.argv) == 2:  # python3 main.py test_create_group
        if str(sys.argv[1]).startswith('test_'):
            pattern = f'{sys.argv[1]}.py'
        elif sys.argv[1] == 'major':  # python3 main.py major
            pattern = 'test_major*.py'
        else:
            pattern = 'test_*.py'
            case_dir = f'./testCase/{sys.argv[1]}'
    else:  # python3 main.py createNoteApi
        pattern = 'test_*.py'
    suite = unittest.TestLoader().discover(case_dir, pattern=pattern)
    result = BeautifulReport(suite)
    res = result.report(filename="report.html", description='测试报告', report_dir='./')
