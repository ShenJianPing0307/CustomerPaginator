from django.utils.safestring import mark_safe

class Paginator(object):

    def __init__(self,totalNum,currentPage,baseUrl,perPageNum=3,maxPageNum=3):
        # 总的数据个数
        self.total_num = totalNum
        # 当前页
        self.current_page = currentPage
        # 访问的baseurl
        self.base_url = baseUrl
        # 每页显示的数据条数
        self.per_page_num = int(perPageNum)
        # 显示的最多页码个数
        self.max_page_num = int(maxPageNum)

    def __repr__(self):

        return "Page %s of %s" % (self.validate_num(self.current_page), self.num_pages)

    @property
    def num_pages(self):
        """
        获取总的页数，总的数据个数%每页显示的个数
        :return:
        另一种计算方法
        a = self.total_num//self.per_page_num 取整
        b = self.total_num%self.per_page_num 取余
        if b == 0
            :return a
        :return a+1
        """
        if self.total_num == 0:
            return 0
        a, b = divmod(self.total_num, self.per_page_num)
        if b == 0:
            return a
        return a + 1

    def validate_num(self, num):
        """
        对页码进行验证，如果不是整数，就让其访问第一页
        :param num:
        :return:
        """
        try:
            num = int(num)
        except Exception as e:
            num = 1
        if num <= 0:
            num = 1
        return num

    def has_previous(self):

        return self.validate_num(self.current_page) >= 1

    def previous_page_num(self):

        return self.validate_num(self.current_page) - 1

    def has_next(self):

        return self.validate_num(self.current_page) <= self.num_pages

    def next_page_num(self):

        return self.validate_num(self.current_page) + 1

    @property
    def start_index(self):
        return (self.validate_num(self.current_page) - 1) * self.per_page_num

    @property
    def end_index(self):
        return self.validate_num(self.current_page) * self.per_page_num

    def get_range_page_num(self):
        """
        self.current_page 当前页
        self.per_pager_num 显示页码的个数
        self.num_pages 总页数
        :return:
        """
        # 1、页码不够多，达不到要求定制的页码个数
        # 如果总页数小于需要显示的页码个数，就将所有的页码全部显示出来
        if self.num_pages < self.per_page_num:
            return range(1, self.num_pages + 1)
        # 2、页码足够多，已经远远超过了要求定制的页码个数
        # half = self.per_pager_num//2
        half = int(self.per_page_num / 2)
        # 左临界条件，如果当前页没有超过显示页码个数的一半，就将定制的页码个数全部显示出来
        if self.validate_num(self.current_page) <= half:
            return range(1, self.per_page_num + 1)
        # 右临界条件，如果点击到最后一个页码
        if (self.validate_num(self.current_page) + half) > self.num_pages:
            return range(
                self.num_pages - self.per_page_num + 1,
                self.num_pages + 1)
        # 中间情况，如果当前页超过显示页码个数的一半，根据当前页计算开始和结束的页码
        return range(self.validate_num(self.current_page) -half,self.validate_num(self.current_page) +half +1)

    def get_range_page__num_str(self):

        page_str_list = []
        # 首页
        first = "<li><a href='%s?p=%s'>首页</a></li>" % (self.base_url, 1)
        page_str_list.append(first)

        # 上一页
        if self.has_previous():
            if self.validate_num(self.current_page) == 1:
                previous = "<li><a href=''>上一页</a></li>"
            else:
                previous = "<li><a href='%s?p=%s'>上一页</a></li>" % (
                    self.base_url, self.previous_page_num())
            page_str_list.append(previous)
        # 中间可选页码
        for i in self.get_range_page_num():
            if self.validate_num(self.current_page) == i:
                temp = "<li class='active'><a href='%s?p=%s'>%s</a></li>" % (self.base_url, i, i)
            else:
                temp = "<li><a href='%s?p=%s'>%s</a></li>" % (self.base_url, i, i)
            page_str_list.append(temp)
        # 下一页
        if self.has_next():
            if self.validate_num(self.current_page) == self.num_pages:
                next = "<li><a href=''>下一页</a></li>"
            else:
                next = "<li><a href='%s?p=%s'>下一页</a></li>" % (
                    self.base_url, self.next_page_num())
            page_str_list.append(next)
        # 尾页
        last = "<li><a href='%s?p=%s'>尾页</a></li>" % (self.base_url, self.num_pages)
        page_str_list.append(last)
        # 统计 Page 2 of 4
        page_of_total = "<li class='disabled'><span>%s</span></li>"%(self.__repr__())
        page_str_list.append(page_of_total)

        return mark_safe(''.join(page_str_list))
