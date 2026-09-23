import pytest
import yaml
import os
import allure
from common.brand_api import BrandApi
from common.assert_util import validate_json_schema
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
    def test_brand_list(self, brand_api,db_util, case):
        with allure.step(f"请求品牌列表：第{case['page_num']}页，每页{case['page_size']}条"):
            response = brand_api.get_brand_list(case['page_num'], case['page_size'])
        with allure.step("断言 HTTP 状态码"):
            assert response.status_code == case['expect_status']
        with allure.step("断言业务返回码"):
            assert response.json()['code'] == case['expect_code']
        with allure.step("断言 JSON Schema 结构"):
            validate_json_schema(response.json(), "brand_list_schema.json")
        with allure.step("数据库校验：接口返回的品牌与数据库一致"):
            res_json = response.json()
            # 只有当接口正常返回且有数据时才去查数据库
            if res_json['code'] == 200 and res_json['data']['list']:
                # 获取接口返回的第一个品牌信息
                api_brand = res_json['data']['list'][0]

                # 去数据库查询（注意：这里用了参数化 %s，防止SQL注入）
                sql = "SELECT id, name, first_letter, sort FROM pms_brand WHERE id = %s"
                db_brand = db_util.query_one(sql, (api_brand['id'],))

                # 断言数据库存在该记录
                assert db_brand is not None, f"数据库中没有找到ID为 {api_brand['id']} 的品牌"
                # 断言字段值与接口返回一致
                assert db_brand['name'] == api_brand['name']
                assert db_brand['first_letter'] == api_brand['firstLetter']
                assert db_brand['sort'] == api_brand['sort']
        # ===================================================
