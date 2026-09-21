from common.request_util import RequestUtil


class BrandApi:
    def __init__(self):
        self.req = RequestUtil()
        self.token = None

    def login(self, username="admin", password="123456"):
        """登录获取 token"""
        response = self.req.request(
            'POST', '/admin/login',
            json={"username": username, "password": password}
        )
        # 从响应中提取 token
        self.token = response.json()['data']['token']
        return response

    def get_brand_list(self, page_num=1, page_size=5):
        """获取品牌列表（需要先登录拿 token）"""
        if not self.token:
            self.login()
        headers = {"Authorization": f"Bearer {self.token}"}
        return self.req.request(
            'GET', '/brand/list',
            params={"pageNum": page_num, "pageSize": page_size},
            headers=headers
        )