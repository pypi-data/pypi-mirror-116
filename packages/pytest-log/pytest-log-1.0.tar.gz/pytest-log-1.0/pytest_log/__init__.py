# @File ：__init__.py.py
# -*- ecoding: utf-8 -*-
# @Time: 2021/8/12 21:49
# @Author: niu run peng
import logging

logging.basicConfig(
    filename='test_log.log',
    filemode='w',
    datefmt='a%, %d, %b, %Y %H:%M:%S',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        # 用例路径
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')
