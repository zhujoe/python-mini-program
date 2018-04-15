from xpinyin import Pinyin
import os
import shutil


def change(path):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            change(filepath)
        else:
            if filename[-3:] == 'gba':
                newname = Pinyin().get_pinyin(filename, ' ')
                os.rename(path + '\\' + filename, path + '\\' + newname)
                print(filename + '[changed]')


def movefile(path, newpath):
    filelist = os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            movefile(filepath, path)
        else:
            if filename[-3:] == 'gba':
                shutil.move(filepath, newpath + '\\' + filename)
                print('[goto]'+ newpath + '\\' + filename)


path = input('输入要转换的文件夹路径：')
change(path)
print('是否合并文件？')
choose = input()
if choose:
    movefile(path, path)
