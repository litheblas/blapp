import logging
import signal
import time
from types import FunctionType
from typing import Optional

import attr
import psutil
import requests

logger = logging.getLogger(__name__)


@attr.dataclass(frozen=True)
class ExternalProcessSignals:
    stop: int = signal.SIGTERM
    suspend: int = signal.SIGTSTP
    resume: int = signal.SIGCONT


@attr.dataclass
class ExternalProcess:
    name: str
    start_process: FunctionType
    url: Optional[str] = None
    is_ready: FunctionType = lambda self: True
    timeout: int = 10
    signals: ExternalProcessSignals = ExternalProcessSignals()
    reap_children: bool = False
    reap_children_recursively: bool = False

    _process = None

    def start(self):
        if self._process is not None:
            return

        process = self.start_process()
        assert isinstance(process, psutil.Popen), 'Use the `psutil.Popen` class (not `subprocess.Popen`)'

        start_time = time.time()

        while True:
            return_code = process.poll()
            if return_code is not None:
                raise OSError(f'Error starting process, exited with return code {return_code}.')

            if self.is_ready(process):
                logger.info(f'[{self.name}] Process started after {time.time() - start_time} seconds.')
                break

            if time.time() > (start_time + self.timeout):
                raise OSError('Process failed to start within timeout period.')

            time.sleep(0.1)

        self._process = process

    def stop(self):
        process = self._process

        if process is None:
            return

        processes_to_stop = [process] + (
            process.children(recursive=self.reap_children_recursively)
            if self.reap_children else []
        )

        for proc in processes_to_stop:
            logger.info(f'[{self.name}] Asking PID {proc.pid} to exit with signal {self.signals.stop}.')

        start = time.time()

        def on_terminate(process):
            logger.info(f'[{self.name}] PID {process.pid} stopped after {time.time() - start} with exit code {process.returncode}.')

        for proc in processes_to_stop:
            proc.send_signal(self.signals.stop)
        psutil.wait_procs(processes_to_stop, timeout=self.timeout, callback=on_terminate)

        self._process = None

    def suspend(self):
        self._process.send_signal(self.signals.suspend)

    def resume(self):
        self._process.send_signal(self.signals.resume)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.stop()


@attr.dataclass(frozen=True)
class ExternalProcessWebserver:
    url: str
    external_process: ExternalProcess

    def suspend(self):
        return self.external_process.suspend()

    def resume(self):
        return self.external_process.resume()


def http_is_responding(url):
    def checker(process):
        try:
            return requests.get(url).ok
        except requests.ConnectionError:
            return False
    return checker


def output_line_contains(stream, text, case_sensitive=False):
    if not case_sensitive:
        text = text.lower()

    def checker(process):
        line = getattr(process, stream).readline().decode('utf-8')

        if not case_sensitive:
            line = line.lower()

        if text in line:
            getattr(process, stream).close()
            return True

        return False

    return checker
