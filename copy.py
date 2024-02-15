# import shutil
#
# if __name__ == '__main__':
#     for i in range(0, 100):
#         # Define source and destination folders
#         source_folder = r'D:\Documents\metamask-chrome-11.8.0'
#         destination_folder = f'D:\\Documents\\Gologin_Profile\\extensions_backup\\ex_{i + 1}'
#
#         # Copy the contents of the source folder to the destination folder
#         try:
#             shutil.copytree(source_folder, destination_folder)
#             print(f"Folder {i + 1} copied successfully!")
#         except shutil.Error as e:
#             print(f"Error: {e}")
#         except OSError as e:
#             print(f"Error: {e}")

from threading import Thread


class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return