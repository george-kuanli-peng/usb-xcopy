import os
import shutil
import sys
import time

import wmi


SOURCE_DIR = 'd:/temp/sermon'
# SOURCE_DIR = 'd:/Documents/belief/服事/幸福小組'


def get_removable_disks():
    c = wmi.WMI()
    disks = []

    for disk in c.Win32_LogicalDisk(DriveType=2):
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


def copy_disk(disk):
    src_files = os.listdir(SOURCE_DIR)
    for f in src_files:
        src_path = os.path.join(SOURCE_DIR, f)
        dst_path = os.path.join(get_disk_root_dir(disk), f)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
    # TODO: checksum


def main():
    disks = get_removable_disks()
    print_disks(disks)
    while True:
        cmd = input('開始複製檔案，請輸入 yes；取消操作，請輸入 no 或直接關閉視窗: ')
        if cmd.strip().lower() == 'yes':
            break
        elif cmd.strip().lower() == 'no':
            print('操作取消')
            sys.exit(0)
        else:
            print('無效的指令: ' + cmd)
    print('開始複製檔案 (操作完成前，請勿關閉視窗)...')
    for disk_i, disk in enumerate(disks, 1):
        time_start = time.time()
        print('寫入磁碟 %s (%d/%d): ' % (disk['DeviceID'], disk_i, len(disks)), end='')
        copy_disk(disk)
        print('寫入完成  ', end='')
        # TODO: checksum
        print('檢查完成  ', end='')
        time_spent = time.time() - time_start
        print('歷時 %d分%d秒' % (int(time_spent/60), time_spent-int(time_spent/60)*60))
    print('所有磁碟寫入完成')
    # TODO: errors writing a subset of disks


if __name__ == '__main__':
    main()
