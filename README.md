# 云测试项目

本项目记录了两个阶段的测试实操：

## 阶段一：云基础与手工测试
- 云服务器（ECS）搭建 Nginx + MySQL
- 对象存储（OSS）上传/下载/权限/分片上传测试
- 产出物：`01-cloud-infra-testing/cloud-test-cases.md`

## 阶段二：接口测试与自动化
- Docker Compose 部署 Mall 电商系统
- Postman 接口测试集 + Charles 抓包
- Python + Requests + Pytest + YAML + Allure 自动化框架
- 产出物：`02-Mall-testing/` 下的代码、数据、Allure 报告

## 技术栈
- 云平台：阿里云 ECS / OSS
- 容器化：Docker / Docker Compose
- 接口测试：Postman / Charles
- 自动化：Python / Pytest / Requests / YAML / Allure