class MockCache:
    """simple cache mock"""
    def __init__(self):
        self.__reset()

    async def clear(self, namespace=None):
        self.cache_cleared = True

    def __is_cleared(self):
        return self.cache_cleared

    def __reset(self):
        self.cache_cleared = True