import tzlocal
class timezone(object):
    @classmethod
    def search(cls):
        return tzlocal.get_localzone().zone
