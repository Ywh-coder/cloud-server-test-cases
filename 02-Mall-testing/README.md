# Mall 电商系统接口自动化测试

## 技术栈
- Python 3.13
- Requests + Pytest + YAML + Allure
- 被测系统：Mall 电商系统（Docker 部署）

## 项目结构
```
02-Mall-testing/
├── common/              # 请求封装、接口封装、环境配置
│   ├── request_util.py  # HTTP 请求封装（含日志、异常处理）
│   ├── login_api.py     # 登录接口封装
│   ├── brand_api.py     # 品牌接口封装（含 token 管理）
│   └── config.yaml      # 多环境配置
├── data/                # YAML 测试数据
│   ├── login_data.yaml
│   └── brand_data.yaml
├── testcases/           # 测试用例
│   ├── test_login.py
│   └── test_brand.py
├── report/              # Allure 报告输出目录
├── conftest.py          # pytest 钩子（注入环境信息 + session 级 fixture）
├── pytest.ini           # pytest 配置
└── requirements.txt
```

## 如何运行
```bash
pip install -r requirements.txt
pytest testcases/ -v
pytest --alluredir=./report/allure-results
allure serve ./report/allure-results
```

## 已覆盖接口
| 模块 | 接口 | 用例数 | 场景 |
|------|------|--------|------|
| 登录 | POST /admin/login | 2 | 正常登录、密码错误 |
| 品牌 | GET /brand/list | 2 | 第1页、第2页 |

## 测试结果
- 4 个用例全部通过
- Allure 报告已生成

## 环境信息
- 被测系统：http://8.163.24.111:8080
- 部署方式：Docker Compose（Mall 电商系统）
## 测试报告截图
![Allure 报告](../assets/Allure-report.png)