# -*- coding: utf-8 -*-

import signal
import socket
import asyncio

import jinja2

from tornado_jinja2 import Jinja2Loader

from tornado import version as tornado_version
from tornado.web import Application
from tornado.options import options
from tornado.process import cpu_count, fork_processes
from tornado.netutil import bind_sockets
from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop

from hagworm import hagworm_slogan
from hagworm import __version__ as hagworm_version
from hagworm.extend.base import Utils
from hagworm.extend.logging import DEFAULT_LOG_FILE_ROTATOR, init_logger
from hagworm.extend.interface import TaskInterface
from hagworm.extend.asyncio.base import install_uvloop
from hagworm.frame.tornado.web import LogRequestMixin


class _LauncherBase(TaskInterface):
    """启动器基类
    """

    def __init__(self, **kwargs):

        self._debug = kwargs.get(r'debug', False)

        self._process_num = kwargs.get(r'process_num', 1)

        self._on_startup = kwargs.get(r'on_startup', None)
        self._on_shutdown = kwargs.get(r'on_shutdown', None)

        self._background_service = kwargs.get(r'background_service', None)
        self._background_process = kwargs.get(r'background_process', None)

        self._process_id = 0
        self._process_num = self._process_num if self._process_num > 0 else cpu_count()

        # 后台服务任务对象
        if self._background_service is None:
            pass
        elif not isinstance(self._background_service, TaskInterface):
            raise TypeError(r'Background Service Dot Implemented Task Interface')

        # 服务进程任务对象，服务进程不监听端口
        if self._background_process is None:
            pass
        elif isinstance(self._background_process, TaskInterface):
            self._process_num += 1
        else:
            raise TypeError(r'Background Process Dot Implemented Task Interface')

        init_logger(
            kwargs.get(r'log_level', r'info').upper(),
            kwargs.get(r'log_handler', None),
            kwargs.get(r'log_file_path', None),
            kwargs.get(r'log_file_rotation', DEFAULT_LOG_FILE_ROTATOR),
            kwargs.get(r'log_file_retention', 0xff),
            self._debug
        )

        environment = Utils.environment()

        Utils.log.info(
            f'{hagworm_slogan}'
            f'hagworm {hagworm_version}\n'
            f'tornado {tornado_version}\n'
            f'python {environment["python"]}\n'
            f'system {" ".join(environment["system"])}'
        )

        install_uvloop()

        self._sockets = None
        self._event_loop = None

    def set_socket_buf(self, *, snd_buf=0, rcv_buf=0):

        for _socket in self._sockets:

            if snd_buf > 0:
                _socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, snd_buf)

            if rcv_buf > 0:
                _socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rcv_buf)

    def start(self):

        if self._on_startup:
            self._event_loop.run_until_complete(self._on_startup())

        if self._background_service is not None:
            self._background_service.start()
            Utils.log.success(f'Background service no.{self._process_id} running...')

        if self._process_id == 0 and self._background_process is not None:
            self._background_process.start()
            Utils.log.success(f'Background process no.{self._process_id} running...')
        else:
            self._server.add_sockets(self._sockets)

        Utils.log.success(f'Startup server no.{self._process_id}')

        self._event_loop.run_forever()

        if self._on_shutdown is not None:
            self._event_loop.run_until_complete(self._on_shutdown())

    def stop(self, code=0):

        if self._background_service is not None:
            self._background_service.stop()

        if self._process_id == 0 and self._background_process is not None:
            self._background_process.stop()

        self._event_loop.stop()

        Utils.log.success(f'Shutdown server no.{self._process_id}: code.{code}')

    def is_running(self):

        return self._event_loop.is_running()


class _Application(Application):

    def log_request(self, handler):

        if isinstance(handler, LogRequestMixin):
            handler.log_request()
            super().log_request(handler)
        elif self.settings.get(r'debug') or handler.get_status() >= 400:
            super().log_request(handler)


class Launcher(_LauncherBase):
    """TornadoHttp的启动器

    用于简化和统一程序的启动操作

    """

    def __init__(self, router, port=80, *, server_settings=None, **kwargs):

        super().__init__(**kwargs)

        self._server_settings = {} if server_settings is None else server_settings

        self._app_settings = {
            r'handlers': router,
            r'debug': self._debug,
            r'gzip': kwargs.get(r'gzip', False),
        }

        if r'template_path' in kwargs:
            self._app_settings[r'template_loader'] = Jinja2Loader(
                jinja2.Environment(
                    loader=jinja2.FileSystemLoader(kwargs[r'template_path'])
                )
            )

        if r'static_path' in kwargs:
            self._app_settings[r'static_path'] = kwargs[r'static_path']

        if r'cookie_secret' in kwargs:
            self._app_settings[r'cookie_secret'] = kwargs[r'cookie_secret']

        self._sockets = bind_sockets(port)

        if self._process_num > 1:
            self._process_id = fork_processes(self._process_num)

        options.parse_command_line()

        AsyncIOMainLoop().install()

        self._event_loop = asyncio.get_event_loop()
        self._event_loop.set_debug(self._app_settings[r'debug'])

        self._event_loop.add_signal_handler(signal.SIGINT, self.stop)
        self._event_loop.add_signal_handler(signal.SIGTERM, self.stop)

        self._server = HTTPServer(_Application(**self._app_settings), **self._server_settings)
