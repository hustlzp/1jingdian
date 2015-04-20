# coding: utf-8
import re
from urlparse import urlparse


def check_url(form, field):
    """检查url schema，若不存在则默认补充http"""
    url = field.data.strip()
    if not url:
        return
    result = urlparse(url)
    if result.scheme == "":
        field.data = "http://%s" % re.sub(r'^:?/*', '', url)


def trim(form, field):
    if field.data and isinstance(field.data, basestring):
        field.data = field.data.strip()
