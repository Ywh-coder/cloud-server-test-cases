import pytest
import yaml
import os
import allure
from common.brand_api import BrandApi


def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'brand_data.yaml')
brand_data = load_yaml(data_path)['brand_cases']


@allure.feature("品牌模块")
class TestBrand:

    @allure.story("品牌列表接口")
    @allure.title("测试品牌列表：{case[case_name]}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("case", brand_data, ids=[c['case_name'] for c in brand_data])
    def test_brand_list(self, brand_api, case):
        with allure.step(f"请求品牌列表：第{case['page_num']}页，每页{case['page_size']}条"):
            response = brand_api.get_brand_list(case['page_num'], case['page_size'])
        with allure.step("断言 HTTP 状态码"):
            assert response.status_code == case['expect_status']
        with allure.step("断言业务返回码"):
            assert response.json()['code'] == case['expect_code']