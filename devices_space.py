from json import loads

from .command_executor import run_command
from .notifier import log_error, log_info


def select_device(nativescript_command, on_device_selected):
    devices = []

    def add_device_if_not_empty(device):
        if device is not None:
            devices.append(device)

    def on_device_data_received(device_data):
        add_device_if_not_empty(_parse_device_data(device_data))

    def on_devices_data_finished(succeeded):
        if succeeded:
            return _show_devices_list_and_select_device(nativescript_command,
                                                        devices,
                                                        on_device_selected)
        else:
            return on_device_selected(None)

    run_command(["device", "--json"],
                on_device_data_received,
                on_devices_data_finished,
                True, "Retrieving devices")


def _parse_device_data(device_data):
    try:
        return loads(device_data)
    except ValueError:
        log_error(device_data)


def _show_devices_list_and_select_device(nativescript_command,
                                         devices,
                                         on_device_selected):
    devicesCount = len(devices)
    if devicesCount == 0:
        log_info("There are no connected devices")
        on_device_selected(None)
    elif devicesCount == 1:
        on_device_selected(devices[0])
    elif devicesCount > 1:
        def get_device_info(device):
            def get_value(prop):
                return device[prop] if device.get(prop) else ""

            display_name = get_value("displayName") or get_value("identifier")
            platform = "Platform: {platform} {version}".format(
                    platform=get_value("platform"),
                    version=get_value("version"))
            model = "Model: {model}".format(model=get_value("model"))
            vandor = "Vendor: {vendor}".format(vendor=device.get("vendor"))
            return [display_name, platform, model, vandor]

        devicesList = list(map(get_device_info, devices))

        nativescript_command.get_window().show_quick_panel(
            devicesList,
            lambda device_index:
            on_device_selected(devices[device_index])
            if device_index >= 0 else on_device_selected(None))
