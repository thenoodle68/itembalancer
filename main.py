import os
import ctypes
import sys
nope = ["System Volume Information","$RECYCLE.BIN"]
dirs = ["d","e","f"]
insert_dirs = ["H:\\downloads\\Complete\\..Done\\"]

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def disk_usage(path):
    _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                       ctypes.c_ulonglong()
    if sys.version_info >= (3,) or isinstance(path, unicode):
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
    else:
        fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
    ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
    if ret == 0:
        raise ctypes.WinError()
    used = total.value - free.value
    return (total.value, used, free.value)


def constructSection(target_directory):
    entries = {}
    alpha_entries = []
    for x in os.listdir(target_directory):
        if x not in nope:
            entries[x] = getFolderSize(target_directory+x)
            alpha_entries.append(x)
    return [entries,alpha_entries]

series = {}
alpha_series = []
dirs.sort()
dirs.reverse()
for x in dirs:
    x += ":\\"
    b = constructSection(x)
    series.update(b[0])
    alpha_series+=b[1]

for x in insert_dirs:
    b = constructSection(x)
    series.update(b[0])
    alpha_series+=b[1]

alpha_series.sort()
alpha_series.reverse()

total_stored = 0
for x in series:
    total_stored += series[x]

total_storage = 0

def sizeOfDirs(dirs):
    total = 0
    for x in dirs:
        total += series[x]
    return total

for x in dirs:
    total_storage += disk_usage(x+":\\")[0]

finished = {}
total_per_drive = total_stored/len(dirs)
alpha_series_cur = alpha_series
for x in dirs:
    this_drive = []
    cont = 1
    while sizeOfDirs(this_drive) < total_per_drive and cont == 1 and len(alpha_series_cur) > 0:
        this_drive.append(alpha_series_cur[0])
        if sizeOfDirs(this_drive) > disk_usage(x+":\\")[0]:
            cont = 0
        else:
            alpha_series_cur = alpha_series_cur[1:]
    finished[x] = this_drive

operations = []
for x in finished:
    for y in finished[x]:
        if not os.path.isdir(x+":\\"+y):
            operations.append((y,x))

# make this do stuff instead
for x in operations:
    print x