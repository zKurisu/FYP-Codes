def next_mac(type, index):
    """ All MAC for AP or Host """
    if type == "host":
        prefix = 0x00
    else:
        prefix = 0x02
    return '%02x:%02x:%02x:%02x:%02x:%02x' % (
        prefix,
        (index >> 32) & 0xff,
        (index >> 24) & 0xff,
        (index >> 16) & 0xff,
        (index >> 8) & 0xff,
        index & 0xff,
    )
