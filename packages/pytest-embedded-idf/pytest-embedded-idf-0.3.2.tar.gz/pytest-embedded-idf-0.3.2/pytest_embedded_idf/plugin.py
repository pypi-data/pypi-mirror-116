import logging
import os
from types import ModuleType

import pytest
from pytest_embedded.dut import Dut

from .app import IdfApp


@pytest.fixture
def app(options, test_file_path) -> IdfApp:
    """
    Uses `options['App']` as kwargs to create instance.
    """
    app_options = options.get('App', {})
    if app_options['app_path'] is None:
        logging.info(f'test_file_path: {test_file_path}')
        app_options['app_path'] = os.path.dirname(test_file_path)
    return IdfApp(**app_options)


def pytest_addoption(parser):
    group = parser.getgroup('embedded')
    group.addoption(
        '--part-tool',
        help='Partition tool path, used for parsing partition table. '
        '(Default: "$IDF_PATH/components/partition_table/gen_esp32part.py"',
    )


@pytest.hookimpl
def pytest_plugin_registered(plugin, manager):
    if not isinstance(plugin, ModuleType) or plugin.__name__ != 'pytest_embedded.plugin':
        return

    plugin.KNOWN_OPTIONS['App'].append('part_tool')
    plugin.ENV['idf'] = True

    if 'esp' in plugin.ENV:
        from pytest_embedded_serial.dut import SerialDut
        from .serial import IdfSerial

        @pytest.fixture
        def serial(app, target, port, pexpect_proc, options):
            serial_options = options.get('Serial', {})
            if target['target']:
                serial_options.update(target)
            if port['port']:
                serial_options.update(port)
            serial_options['pexpect_proc'] = pexpect_proc

            serial = IdfSerial(app, **serial_options)
            try:
                yield serial
            finally:
                serial.close()

        globals()['serial'] = serial

        @pytest.fixture
        def dut(serial, app, pexpect_proc, options) -> SerialDut:
            """
            Uses `options['Dut']` as kwargs to create instance.
            """
            dut_options = options.get('Dut', {})
            dut = SerialDut(serial, app, pexpect_proc, **dut_options)
            try:
                yield dut
            finally:
                dut.close()

        globals()['dut'] = dut
    else:

        @pytest.fixture
        def dut(app, pexpect_proc, options) -> Dut:
            """
            Uses `options['Dut']` as kwargs to create instance.
            """
            dut_options = options.get('Dut', {})
            dut = Dut(app, pexpect_proc, **dut_options)
            try:
                yield dut
            finally:
                dut.close()

        globals()['dut'] = dut
