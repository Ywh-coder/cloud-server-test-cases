import pytest
import yaml
import os
import allure
from common.login_api import LoginApi


def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


# 获取 data 目录下的 yaml 文件
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'login_data.yaml')
login_data = load_yaml(data_path)['login_cases']


@allure.feature("登录模块")
class TestLogin:

    @classmethod
    def setup_class(cls):
        cls.login_api = LoginApi()

    @allure.story("登录接口")
    @allure.title("测试登录：{case[case_name]}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("case", login_data, ids=[c['case_name'] for c in login_data])
    def test_login(self, case):
        with allure.step(f"发送登录请求：{case['username']} / {case['password']}"):
            response = self.login_api.login(case['username'], case['password'])
        with allure.step("断言 HTTP 状态码"):
            assert response.status_code == case['expect_status']
        with allure.step("断言业务返回码"):
            assert response.json()['code'] == case['expect_code']