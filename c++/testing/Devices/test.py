from DeviceBackend import USBDevice

u= USBDevice()
u.set_vendor_id(0xffff)
u.setup()