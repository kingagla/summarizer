import os


def create_directory(directory):
    directory = os.path.abspath(directory).split('/')
    for i in range(2, len(directory) + 1):
        direc = "/".join(directory[:i])
        if not os.path.isdir(direc):
            os.mkdir(direc)

