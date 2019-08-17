# usb-xcopy

Utility for copying files from a source directory to all removable disks on Windows

## Prerequisites

1. OS: Windows 10
1. Python 3.6+
    - To install a portable distribution of Python, follow these steps:
        1. Download zipped file from here: https://sourceforge.net/projects/portable-python/
        1. Double-click on the file and extract the files on your computer
        1. Go to the extracted folder, and double-click on the "Console-Launcher" icon, and run the command `python --version` in the window. If something like "Python 3.x.x" is printed on the screen, the installtion is complete.
1. Python packages:
    - In the python console, run the command `pip install -y pywin32 WMI`

## Configuration

1. Set the copy source directory in main.py. Suppose all files to copy are within the `C:/sermon` directory, set the variable `SOURCE_DIR` as follows:

		SOURCE_DIR="C:/sermon"

## Execution

Start the program by

```
python -u main.py
```

Information of all the removable disks are displayed, something like:

```
磁區 檔案系統   總空間 剩餘空間 磁區序號
==== ======== ======== ======== ========
  E:    FAT32  29548MB  29548MB 8CXXXXXX
  F:    FAT32   7632MB   2091MB 09XXXXXX
開始複製檔案，請輸入 yes；取消操作，請輸入 no 或直接關閉視窗:
```

Ensure all the disks to write are displayed. If any unwanted disk is there, safely remove and unplug that disk and then restart the program. Enter `yes` to proceed if everything is OK.

Then, all the files within the source directory will be copied into the disks shown above one by one. If everything is OK, something like this will be displayed:

```
開始複製檔案，請輸入 yes；取消操作，請輸入 no 或直接關閉視窗: yes
開始複製檔案 (操作完成前，請勿關閉視窗)...
寫入磁碟 E: (1/2): 寫入完成  檢查完成  歷時 19分52秒
寫入磁碟 F: (2/2): 寫入完成  檢查完成  歷時 19分48秒
所有磁碟寫入完成
```

If there is anything wrong during the operation, something like this may be displayed instead (the actual error messages may vary):

```
開始複製檔案，請輸入 yes；取消操作，請輸入 no 或直接關閉視窗: yes
開始複製檔案 (操作完成前，請勿關閉視窗)...
寫入磁碟 E: (1/2): 寫入完成  檢查完成  歷時 19分21秒
寫入磁碟 F: (2/2): 錯誤
有磁碟寫入錯誤:
F: [WinError 183] 當檔案已存在時，無法建立該檔案。: 'F:/App'
```

## Known Problems

1. File checking after writing has not been implemented currently.
