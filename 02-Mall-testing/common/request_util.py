import requests
import yaml
import os
import time
import logging
from logging.handlers import RotatingFileHandler

# 配置日志：控制台 + 文件
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(console)

    file_handler = RotatingFileHandler(
        'test.log', maxBytes=1024 * 1024, backupCount=3, encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(file_handler)


class RequestUtil:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        env = config['env'][config['active_env']]
        self.base_url = env['base_url']
        self.timeout = env['timeout']
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        kwargs.setdefault('timeout', self.timeout)
        logger.info(f"请求: {method} {url}")
        start = time.time()
        try:
            response = self.session.request(method, url, **kwargs)
            elapsed_ms = round((time.time() - start) * 1000, 2)
            try:
                body_preview = response.text[:200]
            except Exception:
                body_preview = "<binary content>"
            logger.info(f"响应: {response.status_code} [{elapsed_ms}ms] {body_preview}")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"请求超时: {url}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {url} - {e}")
            raise