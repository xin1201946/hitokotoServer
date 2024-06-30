import os


def get_data_size():
    return good_look('DATA')


def get_system_size():
    return good_look('templates')


def get_log_size():
    return good_look('logs')


def get_all_size():
    return good_look('./')


def good_look(filepath):
    total = _getFileSize(filepath)
    if total < 1024:
        return round(total, 2), 'Byte'
    else:
        KBX = total / 1024
        if KBX < 1024:
            return round(KBX, 2), 'K'
        else:
            MBX = KBX / 1024
            if MBX < 1024:
                return round(MBX, 2), 'M'
            else:
                return round(MBX / 1024), 'G'


def _getFileSize(filePath):
    total = 0
    with os.scandir(filePath) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += _getFileSize(entry.path)
    return total
