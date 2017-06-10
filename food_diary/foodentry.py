from datetime import date 

class FoodEntry(object):
    BREAKFAST = 0
    MORNING_SNACK = 1
    LUNCH = 2
    AFTERNOON_SNACK = 3
    EVENING_SNACK = 4
    DINNER = 5
    DRINKS = 6
    OTHER = 7

    """docstring for FoodEntry"""
    def __init__(self, arg):
        super(FoodEntry, self).__init__()
        self.arg = arg
        self.date = date.
        self.userId = None
        self.entry = {}


class FoodItem(object):
    """docstring for FoodItem"""
    def __init__(self, arg):
        super(FoodItem, self).__init__()
        self.arg = arg
        self.name = name
        self.size = size
        self.calories = calories
