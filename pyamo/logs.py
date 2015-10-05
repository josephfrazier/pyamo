# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Portions Copyright (C) Philipp Kewisch, 2015

import sys
import urllib

from .utils import AMO_EDITOR_BASE

from urlparse import urljoin
from datetime import datetime

class LogEntry(object):
    # pylint: disable=too-few-public-methods,too-many-instance-attributes

    def __init__(self, session, row):
        self.addonnum = row.attrib['data-addonid']

        dtcell, msgcell, editorcell, _ = row.getchildren()
        nameelem, actionelem = msgcell.getchildren()

        self.date = datetime.strptime(dtcell.text, '%b %d, %Y %I:%M:%S %p')
        self.addonname = nameelem.text.strip()
        self.addonid = urllib.unquote(actionelem.attrib['href'].split('/')[-1]).decode('utf8')
        self.url = urljoin(AMO_EDITOR_BASE, actionelem.attrib['href'])
        self.version = nameelem.tail.strip()
        self.reviewer = editorcell.text.strip()
        self.action = actionelem.text.strip()
        self.session = session

    def __unicode__(self):
        return u'%s %s %s %s %s %s' % (
            self.date, self.reviewer.ljust(20), self.action.ljust(25),
            self.addonid.ljust(30), self.addonname, self.version
        )

    def __str__(self):
        return unicode(self).encode(sys.stdout.encoding, 'replace')
