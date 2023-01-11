# -*- coding: utf-8 -*-

from mailout.manager import Manager


manager = Manager('gmail')

if __name__ == '__main__':
    manager.perform()
