# usb-xcopy

Utility for copying files from a source directory to all removable disks on Windows

## Prerequisites

1. OS: Windows 10
1. Python 3.6+
1. Python packages:
    - In the python console, run the command `pip install pywin32 WMI tqdm`

## Configuration

1. Set the copy source directory in main.py. Suppose all files to copy are within the `C:/sermon` directory, set the variable `SOURCE_DIR` as follows:

		SOURCE_DIR="C:/sermon"

## Execution

Double-click on the "run.bat" file, or start the program by

```
python -u main.py
```

Information of all the removable disks are displayed, something like:

```
磁區 檔案系統   總空間 剩餘空間 磁區序號
==== ======== ======== ======== ========
  E:    FAT32  29548MB  29548MB 8CXXXXXX
  F:    FAT32   7632MB   2091MB 09XXXXXX
開始複製檔案 (yes: 開始 / no: 取消操作)?
```

Ensure all the disks to write are displayed. If any unwanted disk is there, safely remove and unplug that disk and then restart the program. Enter `yes` to proceed if everything is OK.

Then, all the files within the source directory will be copied into the disks shown above one by one. If everything is OK, something like this will be displayed:

```
開始複製檔案 (yes: 開始 / no: 取消操作)? yes
開始複製 1521 個檔案至各磁區 (操作完成前，請勿關閉視窗)...
寫入磁碟 E: (1/1):
Copy: 100%|########################################################################| 1521/1521 [04:57<00:00,  4.07it/s]
歷時 4分57秒
寫入磁碟 F: (1/1):
Copy: 100%|########################################################################| 1521/1521 [05:12<00:00,  4.07it/s]
歷時 5分13秒
所有磁碟寫入完成
```

If there is anything wrong during the operation, something like this may be displayed instead (the actual error messages may vary):

```
開始複製檔案，請輸入 yes；取消操作，請輸入 no 或直接關閉視窗: yes
開始複製檔案 (操作完成前，請勿關閉視窗)...
寫入磁碟 E: (1/1):
Copy: 100%|########################################################################| 1521/1521 [04:57<00:00,  4.07it/s]
歷時 4分57秒
寫入磁碟 F: (2/2): 錯誤
Copy:  38%|###########################6                                             | 576/1521 [02:03<50:55,  3.23s/it]
錯誤
有磁碟寫入錯誤:
F: 寫入檔案數目錯誤: 總數 1521, 實際寫入 576
```

To retry to write the disks with failure during previous operation, remove all the disks that have been written successfully, clean up all the disks to retry, and run the program again.

## Known Problems

1. File checking after writing has not been fully implemented currently; only the number of written files is checked.
