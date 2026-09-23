import os
import yaml
import pytest
from common.brand_api import BrandApi
import pymysql
from common.db_util import DBUtil

@pytest.fixture(scope="session")
def brand_api():
    return BrandApi()

def pytest_sessionstart(session):
    """测试会话开始时，将环境信息写入 Allure 结果目录"""
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'common', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    active_env = config['active_env']
    env_config = config['env'][active_env]

    results_dir = os.path.join(base_dir, 'report', 'allure-results')
    os.makedirs(results_dir, exist_ok=True)

    env_file = os.path.join(results_dir, 'environment.properties')
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(f"Python.Version=3.13.5\n")
        f.write(f"Pytest.Version=9.1.1\n")
        f.write(f"Test.Environment={active_env}\n")
        f.write(f"Base.URL={env_config['base_url']}\n")
        f.write(f"Project=Mall API Automation\n")


@pytest.fixture(scope="session")
def db_util():
    """数据库连接 fixture，session级别，自动管理连接和关闭"""

    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'common', 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    active_env = config['active_env']
    db_config = config['env'][active_env]['db']

    db = DBUtil(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    yield db  # 把 db 对象返回给测试用例使用
    db.close()  # 所有测试执行完毕后，自动关闭连接
