import os

if __name__ == '__main__':
    folder_path = r"D:\Documents\Gologin_Profile\profile"
    os.remove(os.path.join(folder_path, "profile_101"))
    # files = os.listdir(folder_path)
    #
    # count = 1
    # for file in files:
    #     old_path = os.path.join(folder_path, file)
    #     print(old_path)
    #     new_path = os.path.join(folder_path, f"profile_{count}")
    #     print(new_path)
    #     os.rename(old_path, new_path)
    #     count += 1
