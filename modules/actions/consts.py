from enum import Enum


class ActionType(str, Enum):
    PURCHASE = 'purchase'
    VISIT = 'visit'


class ProductType(str, Enum):
    MONITOR = 'monitor'
    PRINTER = 'printer'
    SCANNER = 'scanner'
    LAPTOP = 'laptop'
    TABLET = 'tablet'


class MetricType(str, Enum):
    TOTAL_USERS = 'total_users'
    AVG_DAILY_USERS = 'avg_daily_users'
    TOTAL_PURCHASES = 'total_purchases'
    AVG_DAILY_PURCHASES = 'avg_daily_purchases'
