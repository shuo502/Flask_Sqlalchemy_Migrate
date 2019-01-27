#conding=utf-8
__author__ = 'yo'
from app import apps
import os
@apps.route('/favicon/<int:id>')
def favicon(id):
    id=int(id)
    # entries = markbook.filter(markbook.id == id)[0]
    # b=entries.links
    b=""
    c=b.find('/',8)
    if c>0:
        host=str(b[:c])
    else:
        host =str(b)
    icon=host+'/favicon.ico'
    file=str(id)+'_favicon.ico'
    if os.path.exists(file):
        return icon
    return icon
apps.add_template_filter(favicon,'favicon')
