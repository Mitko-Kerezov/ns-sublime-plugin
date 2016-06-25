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
