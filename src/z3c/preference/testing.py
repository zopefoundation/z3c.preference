##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi

import z3c.preference


class BrowserLayer(zope.testbrowser.wsgi.Layer,
                   zope.app.wsgi.testlayer.BrowserLayer):
    """BrowserLayer which is compatible with zope.testbrowser."""

    def testSetUp(self):
        super().testSetUp()
        self._application.requestFactory._db = self.db

    def testTearDown(self):
        self._application.requestFactory._publication_cache.clear()
        super().testTearDown()

    make_wsgi_app = zope.app.wsgi.testlayer.BrowserLayer.make_wsgi_app


Layer = BrowserLayer(z3c.preference)
