#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main app to start Tornado Web Server

@datecreated: 2019-08-13
@lastupdated: 2019-11-12
@author: luisjba
"""
# Meta informations.
__author__ = 'Jose Luis Bracamonte Amavizca'
__version__ = '0.1.0'
__maintainer__ = 'Jose Luis Bracamonte Amavizca'
__email__ = 'me@luisjba.com'
__status__ = 'Development'

import os, signal
from log import logger
import misc, utils, mvc
from mvc import MVCTornadoApp
# from zmq import eventloop
# eventloop.ioloop.install()

if __name__ == "__main__":
    import argparse
    config = misc.Config()
    conf_keys = ["app_name", "home_controller", "controllers_path","views_path","assets_path","db_connections","app_config"]
    app_kwargs = {conf_k:config.get(conf_k) for conf_k in conf_keys}
    # app_kwargs["zmq_eventloop"] = eventloop
    app_kwargs["logger"] = logger
    pidfile_path = config.get('pid_file')
    parser = argparse.ArgumentParser(description='Launch a {} web server'.format(app_kwargs["app_name"]), formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-p', '--port', type=int, default=8888, help='port to launch the server')
    parser.add_argument('-b', '--baseurl', default="", help="base url")
    parser.add_argument('--interface', default=None, help="interface to listen on (default all)")
    args = parser.parse_args()
    logger.info("starting tornado web server")
    pidlock = mvc.get_pid_lock_file(pidfile_path, logger, app_kwargs["app_name"])
    pidlock.acquire(timeout=10)
    app = MVCTornadoApp(args.baseurl,  **app_kwargs)
    listen = {'port': args.port, 'xheaders': True}
    if args.interface is not None:
        listen['address'] = mvc.get_ip_address(args.interface)
    logger.info("Listening configuration: %s", listen)
    
    def handler(signum, frame):
        logger.info("Received %s, shutting down...", signum)
        app.stop()
    
    signal.signal(signal.SIGHUP, handler)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    
    app.listen(**listen)
    app.start()
    pidlock.release()
    logger.info('{} server stopped'.format(app_kwargs["app_name"]))
