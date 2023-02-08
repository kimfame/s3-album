from rest_framework.pagination import LimitOffsetPagination

class PictureLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10