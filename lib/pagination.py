import math


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11,
                 position='pos'):
        """
        current_page 当前页码
        all_count 数据库中的总条数
        base_url 原始 URL
        query_params 保留原搜索条件
        per_page 一页展示多少条
        pager_page_count 最多显示多少个页码
        """

        self.all_count = all_count
        self.per_page = per_page
        self.position = position

        # 计算一共有多少个页码
        # 1.取余
        # 100 / 9  11 1
        # 100 / 10  10 0
        # div, p = divmod(all_count, per_page)
        # if p != 0:
        #     div += 1
        # self.current_count = div

        # 2. 进位
        self.current_count = math.ceil(all_count / per_page)

        # 1. 只能是满足条件的数字
        try:
            self.current_page = int(current_page)
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:
            self.current_page = 1

        self.base_url = base_url
        self.query_params = query_params

        self.pager_page_count = pager_page_count
        # 分页的中值
        self.half_pager_count = int(self.pager_page_count / 2)
        if self.current_count < self.pager_page_count:
            # 如果可分页的页码小于最大显示页码，就让最大显示页码变成可分页页码
            self.pager_page_count = self.current_count

    def page_html(self):
        # 计算页码的起始和结束
        # 分类讨论
        # 1. 正常情况
        # 20  9    4 5 6 7 8 9 10 11 12 13 14
        start = self.current_page - self.half_pager_count
        end = self.current_page + self.half_pager_count
        if self.current_page <= self.half_pager_count:
            # 在最左侧
            start = 1
            # 右边就是最大值
            end = self.pager_page_count
        if self.current_page + self.half_pager_count >= self.current_count:
            # 在最右侧
            start = self.current_count - self.pager_page_count + 1
            end = self.current_count

        # 生成分页
        page_list = []

        # 上一页
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">上一页</a></li>')

        # 数字部分
        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">{i}</a></li>'
            page_list.append(li)

        # 下一页
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}#{self.position}">下一页</a></li>')

        if len(page_list) == 1:
            # 不显示分页器
            page_list = []
        return ''.join(page_list)

    @property
    def query_encode(self):
        return self.query_params.urlencode()

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

# if __name__ == '__main__':
#     # 1 2 3 4 5 6 7 8 9 10
#     # 1  0  2      [((页码-1)*每页展示的条数):页码*每页展示的条数]
#     # 2  2  4
#     # 5  8  10
#     pager = Pagination(
#         current_page=1,
#         all_count=100,
#         base_url='/article',
#         query_params={'tag': 'python', 'name': '张三'},
#         per_page=5,
#         pager_page_count=7
#     )
#     # print(pager.start, pager.end)
#     print(pager.page_html())
