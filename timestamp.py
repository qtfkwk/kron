import tzlocal
import pytz
class timezone(object):
    @classmethod
    def search(cls, name=None):
        if name == None:
            return tzlocal.get_localzone().zone
        if name in pytz.all_timezones:
            return name
        name_ = name.lower()
        matches = []
        for t in pytz.all_timezones:
            t_ = t.lower()
            if name_ == t_:
                return t
            if name in t or name_ in t_:
                matches.append(t)
        if len(matches) == 1:
            return matches[0]
        else:
            return matches
    def __init__(self):
        self.original = None
        self.name = self.search()
        self.pytz = pytz.timezone(self.name)
