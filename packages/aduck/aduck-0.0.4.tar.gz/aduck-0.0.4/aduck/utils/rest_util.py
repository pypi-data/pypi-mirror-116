from datetime import datetime


class Response:
    def __init__(self, state=0, content=None):
        self.state = state
        self.content = content


class ErrorResponse(Response):
    def __init__(self, state=0, content=None, message: str = None, details=None):
        super(ErrorResponse, self).__init__(state, content)
        self.state = state
        self.content = content
        self.time = datetime.now()
        self.message = message
        self.details = details


class Limit:
    def __init__(self, page_index, page_size):
        self.page_index = page_index
        self.page_size = page_size

    def mysql(self):
        if self.page_size == -1:
            return ""
        return f" limit {self.page_index * self.page_size},{self.page_size}"

    def mssql(self):
        if self.page_size == -1:
            return ""
        return f" offset {self.page_index * self.page_size} rows fetch next {self.page_size} rows only"

    def postgre(self):
        if self.page_size == -1:
            return ""
        return f" limit {self.page_size} offset {self.page_index * self.page_size}"


class Page:
    def __init__(self, items, total, page_index, page_size):
        self.items = items
        self.total = total
        self.page_index = page_index
        self.page_size = page_size
        self.page_count = 0
        if page_size != 0:
            self.page_count = total // page_size
            if total != self.page_count * page_size:
                self.page_count += 1
