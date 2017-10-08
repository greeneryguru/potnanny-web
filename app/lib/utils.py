import re


class WeekdayMap(object):
    """
    Map days of the week to numbers.
    Used to store day-of-week schedules in a single number.

    Usage:
        dw = WeekdayMap()
        print dw.ordered_list()
        print dw.reverse_ordered_list()
        print dw.get_dict()

    Abbreviation. 
      To truncate the day of week to first 2 or 3 letters, set the 'show_first' 
      option to the number of letters.

        dw = WeekdayMap(show_first=2)

        If you want the un-modified day tags, access the dict at WeekdayMap.data

    """
    def __init__(self, **kwargs):
        self.data = {
            64:     'Sunday',
            32:     'Monday',
            16:     'Tuesday',
            8:      'Wednesday',
            4:      'Thursday',
            2:      'Friday',
            1:      'Saturday',
        }
        self.show_first = None

        for k, v in kwargs.items():
            setattr(self, k, v)


    """
    get the mapping dict. if  show_first was set at creation, the weekdays
    will be abbreviated,

    params:
        none

    returns:
        a dict
    """
    def get_dict(self):
        d = {}
        for val, name in self.data.items():
            if self.show_first:
                name = ''.join( list(name)[0:self.show_first] )

            d.update({val: name})
                
        return d


    """
    get list with mapping of weekdays to values

    params:
        boolean (true = reverse sorting, false[default] = regular sort)

    returns:
        a list or tuples, containing [(abbreviation, number), ]  
    """
    def ordered_list(self, reverse=False):
        l = []
        d = self.get_dict()
        for k in sorted(d.keys(), reverse=reverse):
            l.append((d[k], k))
        
        return l


    """
    same as ordered_list(), but returns in reverse oder
    """
    def reverse_ordered_list(self):
        return self.ordered_list(True) 
        

    def day_value(self, wkday):
        for k, v in self.data:
            if re.search(wkday, v, re.IGNORECASE):
                return k
        
        return None


