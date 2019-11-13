# -*- coding: utf-8 -*-
"""
Home Handler for tornado web server.
@datecreated: 2019-08-13
@lastupdated: 2019-11-13
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.0.1'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'


import functools
import os
import json
import tornado.gen
import tornado.ioloop
import tornado.web
from tornado.web import MissingArgumentError
from datetime import datetime
from mvc import decorator_request_handler_initialize, decorator_request_handler_prepare, decorator_request_handler_render

class IndexRequestHandler(tornado.web.RequestHandler):
    """
    The index request handler render the view views/{controller_name}/index.html
    """
    @decorator_request_handler_initialize
    def initialize(self, **kwargs):
         #do some initialization if needed
        pass

    @decorator_request_handler_prepare
    def prepare(self):
        #Always called no matter which HTTP method is used
        self.model = []

    @decorator_request_handler_render
    def get(self):
        return self.model

    @decorator_request_handler_render
    def post(self):
        return self.model


class ShowRequestHandler(tornado.web.RequestHandler):
    """
    The show request handler render the view views/{controller_name}/show.html
    """
    @decorator_request_handler_initialize
    def initialize(self, **kwargs):
        pass

    @decorator_request_handler_prepare
    def prepare(self):
        self.model = []

    @decorator_request_handler_render
    def get(self):
        return self.model

    @decorator_request_handler_render
    def post(self):
        return self.model
        
class EditRequestHandler(tornado.web.RequestHandler):
    """
    The edit request handler render the view views/{controller_name}/edit.html
    """
    @decorator_request_handler_initialize
    def initialize(self, **kwargs):
        pass

    @decorator_request_handler_prepare
    def prepare(self):
        self.model = []

    @decorator_request_handler_render
    def get(self):
        return self.model

    @decorator_request_handler_render
    def post(self):
        return self.model

class DeleteRequestHandler(tornado.web.RequestHandler):
    """
    The delete request handler render the view views/{controller_name}/delete.html
    """
    @decorator_request_handler_initialize
    def initialize(self, **kwargs):
        pass

    @decorator_request_handler_prepare
    def prepare(self):
        self.model = []

    @decorator_request_handler_render
    def get(self):
        return self.model

    @decorator_request_handler_render
    def post(self):
        return self.model