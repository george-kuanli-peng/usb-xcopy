import os
import shutil
import sys
import time

import tqdm
import wmi


SOURCE_DIR = 'd:/tools/AudacityPortable'


def get_removable_disks():
    c = wmi.WMI()
    disks = []

    for disk in c.Win32_LogicalDisk(DriveType=2):
        if not disk.FileSystem or \
           (isinstance(disk.MediaType, int) and (1 <= disk.MediaType <= 10 or 12 <= disk.MediaType <= 22)):
            continue
        disks.append({
            'Caption': disk.Caption,
            'DeviceID': disk.DeviceID,
            'FileSystem': disk.FileSystem,
            'FreeSpace': disk.FreeSpace,
            'Size': disk.Size,
            'VolumeDirty': disk.VolumeDirty,
            'VolumeName': disk.VolumeName,
            'VolumeSerialNumber': disk.VolumeSerialNumber
        })
    return disks


def print_disks(disks):
    print('磁區 檔案系統   總空間 剩餘空間 磁區序號')
    print('==== ======== ======== ======== ========')
    for disk in disks:
        print('%4s %8s %6dMB %6dMB %8s' % (
            disk['DeviceID'],
            disk['FileSystem'],
            int(disk['Size'])/(1024*1024),
            int(disk['FreeSpace'])/(1024*1024),
            disk['VolumeSerialNumber']
        ))


def get_disk_root_dir(disk):
    return disk['DeviceID'] + '/'


def copy_disk(disk, copy_func=shutil.copy2):
    src_files = os.listdir(SOURCE_DIR)
    for f in src_files:
        src_path = os.path.join(SOURCE_DIR, f)
        dst_path = os.path.join(get_disk_root_dir(disk), f)
        if os.path.isfile(src_path):
            copy_func(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, copy_function=copy_func)
    # TODO: checksum


def get_num_files(root_dir):
    return sum([len(files) for _, _, files in os.walk(root_dir)])


class CopyFileWithProgress(object):
    def __init__(self, num_all_files, pb=None):
        self._num_all_files = num_all_files
        self._num_curr_files = 0
        self._pb = pb

    def __enter__(self):
        self._pb = tqdm.tqdm(total=self._num_all_files, desc='Copy', mininterval=1.0, ascii=True)
        return self

    def __exit__(self, *exc):
        self._pb.close()
        self._pb = None

    def __call__(self, src, dst):
        shutil.copy2(src, dst)
        self._num_curr_files = self._num_curr_files + 1
        self._pb.update(1)


def main():
    errs = []
    disks = get_removable_disks()
    print_disks(disks)
    while True:
        cmd = input('開始複製檔案 (yes: 開始 / no: 取消操作)? ')
        if cmd.strip().lower() == 'yes':
            break
        elif cmd.strip().lower() == 'no':
            print('操作取消')
            sys.exit(0)
        else:
            print('無效的指令: ' + cmd)
    num_files = get_num_files(SOURCE_DIR)
    print('開始複製 %d 個檔案至各磁區 (操作完成前，請勿關閉視窗)...' % num_files)
    for disk_i, disk in enumerate(disks, 1):
        try:
            time_start = time.time()
            print('寫入磁碟 %s (%d/%d): ' % (disk['DeviceID'], disk_i, len(disks)))
            with CopyFileWithProgress(num_files) as copy_func:
                copy_disk(disk, copy_func=copy_func)
            time_spent = time.time() - time_start
            print('歷時 %d分%d秒' % (int(time_spent/60), time_spent-int(time_spent/60)*60))
        except Exception as e:
            print('錯誤')
            errs.append((disk, e))

    if not errs:
        print('所有磁碟寫入完成')
    else:
        print('有磁碟寫入錯誤:')
        for disk, e in errs:
            print(disk['DeviceID'] + ' ' + str(e))


if __name__ == '__main__':
    main()
