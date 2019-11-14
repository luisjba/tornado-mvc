#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model View Controller core framework for Tornado Web Server

@datecreated: 2019-08-13
@lastupdated: 2019-11-13
@author: luisjba
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.1.0'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'

import os, sys, inspect, importlib, utils
import psutil, fcntl, socket, struct
import tornado.web
from tornado.web import url
from functools import wraps
from lockfile.pidlockfile import PIDLockFile

def decorator_request_handler_initialize(func):
    """Initialize the RequestHandler to set the principal attributes and generate the template file """
    @wraps(func)
    def decorator(self, *args, **kwargs):
        for k,v in kwargs.items():
            if k in ['controller_name', 'action_name','logger','db']:
                self.__setattr__(k,v)
        if 'controller_name' in kwargs.keys() and 'action_name' in kwargs.keys():
            self.template_file = "{}/{}.html".format(self.controller_name, self.action_name )
        if 'logger' in kwargs.keys() and self.logger is None:
            self.logger = importlib.import_module('log').logger
        func(self, *args, **kwargs)
    return decorator

def decorator_request_handler_prepare(func):
    "prepare the RequestHandler when a request is received"
    @wraps(func)
    def decorator(self, *args, **kwargs):
        self._db = self.db()
        self.cursor = None
        if self._db is not None:
            self.cursor = self._db.cursor(dictionary=True)
        self.is_ajax_request = False
        if self.request.headers.get("X-Requested-With", "").startswith("XMLHTTPRequest"):
            self.is_ajax_request = True
        self.response = {'status':'ok'}
        func(self, *args, **kwargs)
    return decorator

def decorator_request_handler_render(func):
    "perform the render for RequestHandler when a get or post is requested"
    @wraps(func)
    def decorator(self, *args, **kwargs):
        function_ret = func(self, *args, **kwargs)
        render_kwargs = {"controller_name": self.controller_name, 
            "action_name": self.action_name,
            "model": {}
        }
        if function_ret is not None and type(function_ret) is tuple:
            if len(function_ret) > 0 :
                model_idx = 0
                # check if the function returns custom template in the first arg
                if type(function_ret[0]) is str:
                    if "/" in function_ret[0] :
                        self.template_file = "{}.html".format(function_ret[0])
                    else:
                        self.template_file = "{}/{}.html".format(self.controller_name, function_ret[0])
                    model_idx = 1
                render_kwargs["model"] = function_ret[model_idx]
                if len(function_ret) > (model_idx + 1) and type(function_ret[(model_idx + 1)]) is dict:
                    for k,v in function_ret[(model_idx + 1)].items() :
                        if not "model" == k:
                            render_kwargs[k] = v
        else:
            render_kwargs["model"] = function_ret
        if self.logger is not None:
            self.logger.info("Rendered template:{}".format(self.template_file),render_kwargs)
            # self.logger.info(render_kwargs)
        self.render(self.template_file, **render_kwargs)
    return decorator

    
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def get_pid_lock_file(pidfile_path, logger, app_name):
    pidlock = PIDLockFile(pidfile_path)
    if pidlock.is_locked():
        old_pid = pidlock.read_pid()
        logger.info("Lock file exists for PID %d." % old_pid)
        if os.getpid() == old_pid:
            logger.info("Stale lock since we have the same PID.")
        else:
            try:
                old = psutil.Process(old_pid)
                if os.path.basename(__file__) in old.cmdline():
                    try:
                        logger.info("Trying to terminate old instance...")
                        old.terminate()
                        try:
                            old.wait(10)
                        except psutil.TimeoutExpired:
                            logger.info("Trying to kill old instance.")
                            old.kill()
                    except psutil.AccessDenied:
                        logger.error("The process seems to be %s, but "
                                     "can not be stopped. Its command line: %s"
                                     % app_name, old.cmdline())
                else:
                    logger.info("Process does not seem to be {}.".format(app_name))
            except psutil.NoSuchProcess:
                pass
                logger.info("No such process exist anymore.")
        logger.info("Breaking old lock.")
        pidlock.break_lock()
    return pidlock 


class MVCTornadoApp(tornado.web.Application):
    def __init__(self, baseurl, zmq_eventloop=None, logger=None, 
                app_name="MVC Tornado App" , home_controller="home", 
                controllers_path="controllers", views_path="views", 
                assets_path="assets",
                db_connections=dict(),
                app_config = dict(),
                db_module_name=""
                ):
        self.baseurl = baseurl.rstrip('/')
        if zmq_eventloop is None:
            zmq_eventloop = importlib.import_module('zmq.eventloop')
            zmq_eventloop.ioloop.install()
        self.logger = logger   
        if self.logger is None:
            self.logger = importlib.import_module('log').logger
        self.db_driver_ready=False
        if not db_module_name == "" and type(db_module_name) is str:
            try:
                self.db_driver = importlib.import_module(db_module_name)
                self.db_driver_error = self.db_driver.Error
                self.db_driver_ready=True
            except :
                self.db_driver_ready=False
        self.app_name = app_name
        self.home_controller = home_controller
        self.controllers_path = controllers_path
        self.views_path = views_path
        self.assets_path = assets_path
        self._db_connections = db_connections
        self.app_config = app_config
        self.base_path = str(os.path.dirname(os.path.abspath(__file__)) ).replace(os.getcwd()+"/","")
        settings = dict(
            compress_response = True,
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.views_path),
            static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.assets_path ),
            debug = True
            )
        self.ioloop = zmq_eventloop.IOLoop.instance()
        # to check for blocking when debugging, uncomment the following
        # and set the argument to the blocking timeout in seconds
        #self.ioloop.set_blocking_log_threshold(.5)
        super(MVCTornadoApp, self).__init__(self.generate_tornado_url_list(), **settings)
        logger.info(f'{self.app_name} Server started')
        try:
            from systemd.daemon import notify
            logger.debug('notifying systemd that we are ready')
            notify('READY=1\nMAINPID={}'.format(os.getpid()), True)
        except ImportError:
            pass

    def get_controllers_module(self,controllers_path='controllers'):
        """
        Find all the controllers and import the module
        
        :param: controllers_path:str
        :rtype:dict
        """
        sufix_filter = "_controller.py"
        size_to_remove = len(sufix_filter) - len(".py")
        controllers_path_abs = controllers_path
        if not controllers_path_abs[0] == "/":
            controllers_path_abs = os.path.join(self.base_path, controllers_path)
        controller_files = [utils.remove_extension(os.path.basename(f)) for f in utils.file_list_by_extension(controllers_path_abs, 'py') if f.endswith(sufix_filter)]
        controllers_module = {}
        for controller_file in controller_files :
            module_name = "{}.{}".format(controllers_path,controller_file)
            controller_name = controller_file[:-size_to_remove]
            controllers_module[controller_name] = {"module":importlib.import_module(module_name), "controller_file":controller_file }
        return controllers_module

    def _extract_controller_actions(self,controller_module):
        sufix_filter = "RequestHandler"
        size_to_remove = len(sufix_filter)
        actions_classes = [member_class for member_class in inspect.getmembers(controller_module, inspect.isclass) if member_class[0].endswith(sufix_filter)]
        controller_actions = {}
        for action_class in actions_classes:
            class_name = action_class[0]
            action_name = class_name[:-size_to_remove].lower()
            controller_actions[action_name] = {"class": action_class[1], "class_name":class_name}
        return controller_actions

    def generate_tornado_url_list(self):
        self._generate_db_connections()
        url_list = []
        for controller_name, controller_module in self.get_controllers_module(self.controllers_path ).items():
            for action_name, action_class in self._extract_controller_actions(controller_module['module']).items():
                # route as raw string 'r'
                url_route =   r"/{}".format(controller_name)
                url_name = r"{}.{}".format(controller_name, action_name)
                if not action_name == "index":
                    url_route = r"/{}/{}/(?P<id>[^\/]+)".format(controller_name, action_name)
                elif controller_name == self.home_controller:
                    url_route = "/"
                    url_name = "home"
                handler_initialize_dict = {
                    "controller_name":controller_name, 
                    "action_name":action_name, 
                    "logger":self.logger,
                    "db": self.get_db
                    }
                url_list.append(url(url_route, action_class["class"], handler_initialize_dict, name=url_name))
        return url_list
    
    def _generate_db_connections(self):
        self.dbs = {}
        self.db = None
        if self.db_driver_ready:
            if type(self._db_connections ) is dict:
                for con_name, con_settings in self._db_connections.items():
                    try :
                        db_con = self.get_db_connection(con_settings)
                        self.dbs[con_name] = db_con
                        self.logger.info("Connected to: {}".format(self.get_db_connection_name(db_con)))
                        if self.db is None or con_name == "default":
                            self.db = db_con
                    except self.db_driver_error as error:
                        self.logger.info(error)
            else:
                self.logger.info("The db_connections is not dict: {}".format(self._db_connections ))

    def get_db_connection(self,connection_settings):
        db_con = None
        if self.db_driver_ready:
            if type(connection_settings) is dict:
                try:
                    db_con = self.db_driver.connect(**connection_settings)
                    return db_con
                except self.db_driver_error as error:
                    print("Error connecting to: {}".format(connection_settings))
                    self.logger.info("Error connecting to: {}".format(connection_settings))
                    raise Exception(error)
                finally:
                    if db_con is not None and  db_con.is_connected():
                        db_con.close()
            else:
                raise Exception('The connection_settings parameter must be a dictionaty with host, , database, user and password')
    
    def get_db(self,con_name='default'):
        if not self.db_driver_ready:
            return None
        if con_name in self.dbs.keys():
            if not self.dbs[con_name].is_connected():
                self.logger.info("Recconectiong to: {}".format(self.get_db_connection_name(self.dbs[con_name])))
                self.dbs[con_name].connect()
            #self.logger.info("Returnning connection: {}".format(self.get_db_connection_name(self.dbs[con_name])))
            return self.dbs[con_name]
        raise Exception('Database Connection {} not exists'.format(con_name))
    
    def get_db_connection_name(self, db_con):
        if self.db_driver_ready:
            return "mysql://{}/{}".format(db_con._host, db_con._database)
        return ""
    
    def start(self):
        self.ioloop.start()

    def stop(self):
        if self.dbs is not None and type(self.dbs) is dict:
            for con_name, db_con in self.dbs.items():
                if db_con.is_connected():
                    self.logger.info("Clossing connection: {}".format(self.get_db_connection_name(db_con)))
                    db_con.close()
        self.ioloop.stop()


