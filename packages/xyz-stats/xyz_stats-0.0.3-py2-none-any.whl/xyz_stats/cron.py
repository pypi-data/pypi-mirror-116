# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_util.dateutils import get_next_date
from . import models
import logging

log = logging.getLogger('django')

def daily_do_stats(the_date=None):
    if not the_date:
        the_date = get_next_date(None, -1)
    for r in models.Report.objects.filter(is_active=True):
        try:
            r.stat(dict(the_date=the_date.isoformat()))
        except:
            import traceback
            log.error('daily_do_stats  report %s error:%s', r, traceback.format_exc())