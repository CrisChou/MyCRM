class Pagefunc:
    '''
        current_page:当前页
    '''

    def __init__(
            self,
            current_page,
            all_count,
            filter_ele,
            sorted_ele,
            data_num=None,
            show_page=11, ):
        try:
            self.current_page = int(current_page)
        except:
            self.current_page = 1
        self.data_num = 5 if data_num is None else data_num
        a, b = divmod(all_count, self.data_num)
        if b:
            a = a + 1
        self.all_page = a
        self.show_page = show_page
        self.filter_ele = filter_ele if filter_ele else ''
        self.sorted_ele = sorted_ele if sorted_ele else ''
        print(self.sorted_ele)

    @property
    def start(self):
        return (self.current_page - 1) * self.data_num

    @property
    def stop(self):
        return self.current_page * self.data_num

    def page(self):
        html_list = []
        half = int((self.show_page - 1) / 2)
        start = 0
        stop = 0
        if self.all_page < self.show_page:
            start = 1
            stop = self.all_page
        else:
            if self.current_page < half + 1:
                start = 1
                stop = self.show_page
            else:
                if self.current_page >= self.all_page - half:
                    start = self.all_page - 10
                    stop = self.all_page
                else:
                    start = self.current_page - half
                    stop = self.current_page + half
        if self.current_page <= 1:

            previous = "<li><a href='#'>Previous</a></li>"
        else:
            previous = "<li><a href='?page=%s%s%s'>Previous</a></li>" % (
                self.current_page - 1, self.filter_ele, self.sorted_ele, )
        html_list.append(previous)
        for i in range(start, stop + 1):
            if self.current_page == i:
                temp = """<li><a href='?page=%s%s%s' style='background-color: 
                red;'>%s</a></li>""" % (i, self.filter_ele, self.sorted_ele, i)
            else:
                temp = "<li><a href='?page=%s%s%s'>%s</a></li>" % (
                    i, self.filter_ele, self.sorted_ele, i)
            html_list.append(temp)
        if self.current_page >= self.all_page:
            nex = "<li><a href='#'>Next</a></li>"
        else:
            nex = "<li><a href='?page=%s%s%s'>Next</a></li>" % (
                self.current_page + 1, self.filter_ele, self.sorted_ele,)
        html_list.append(nex)
        return ''.join(html_list)