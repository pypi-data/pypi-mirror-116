from types import ModuleType
from typing import Optional

import pytest

from .dut import SerialDut
from .serial import Serial


@pytest.fixture
def port(request) -> dict[str, Optional[str]]:
    """
    Apply parametrization to fixture `serial`
    """
    return {'port': getattr(request, 'param', None)}


@pytest.fixture
def serial(port, pexpect_proc, options) -> Serial:
    """
    Uses `options['Serial']` as kwargs to create instance.

    Returns:
        `Serial` instance
    """
    serial_options = options.get('Serial', {})
    if port['port']:
        serial_options.update(port)
    serial_options['pexpect_proc'] = pexpect_proc

    serial = Serial(**serial_options)
    try:
        yield serial
    finally:
        serial.close()


@pytest.fixture
def dut(serial, app, pexpect_proc, options) -> SerialDut:
    """
    Uses `options['Dut']` as kwargs to create instance.

    Returns:
        `SerialDut` instance
    """
    dut_options = options.get('Dut', {})
    dut = SerialDut(serial, app, pexpect_proc, **dut_options)
    try:
        yield dut
    finally:
        dut.close()


def pytest_addoption(parser):
    group = parser.getgroup('embedded')
    group.addoption('--port', help='serial port. Could be overridden by pytest parametrizing. (Default: "None")')


@pytest.hookimpl
def pytest_plugin_registered(plugin, manager):
    if not isinstance(plugin, ModuleType) or plugin.__name__ != 'pytest_embedded.plugin':
        return

    plugin.KNOWN_OPTIONS['Serial'].append('port')
    plugin.ENV['serial'] = True
