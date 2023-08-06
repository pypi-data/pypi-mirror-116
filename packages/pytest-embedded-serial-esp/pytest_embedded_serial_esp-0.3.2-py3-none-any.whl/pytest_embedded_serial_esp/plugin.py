from types import ModuleType
from typing import Optional

import pytest
from pytest_embedded_serial.dut import SerialDut

from .serial import EspSerial


@pytest.fixture
def target(request) -> dict[str, Optional[str]]:
    """
    Apply parametrization to fixture `serial`
    """
    return {'target': getattr(request, 'param', None)}


@pytest.fixture
def port(request) -> dict[str, Optional[str]]:
    """
    Apply parametrization to fixture `serial`
    """
    return {'port': getattr(request, 'param', None)}


@pytest.fixture
def serial(target, port, pexpect_proc, options) -> EspSerial:
    """
    Uses `options['Serial']` as kwargs to create instance.

    Returns:
        `EspSerial` instance
    """
    serial_options = options.get('Serial', {})
    if target['target']:
        serial_options.update(target)
    if port['port']:
        serial_options.update(port)
    serial_options['pexpect_proc'] = pexpect_proc

    serial = EspSerial(**serial_options)
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
    group.addoption(
        '--target', help='serial target chip type. Could be overridden by pytest parametrizing. (Default: "auto")'
    )


@pytest.hookimpl
def pytest_plugin_registered(plugin, manager):
    if not isinstance(plugin, ModuleType) or plugin.__name__ != 'pytest_embedded.plugin':
        return

    plugin.KNOWN_OPTIONS['Serial'].append('target')
    plugin.ENV['esp'] = True
