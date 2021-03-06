#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging


def add2(item, mpc):
    """
    主要入口
    """
    items = listall2(item, mpc)
    items = _filter(items, mpc)
    return items


def _filter(items, mpc):
    occupied = []
    playlists = []
    for item in items:
        if 'playlist' in item:
            try:
                # result+=mpc.listplaylistinfo(item['playlist'])
                occupied += mpc.listplaylist(item['playlist'])
                playlists.append(item)
            except BaseException:
                # tak文件会归类为playlist,但是似乎无法list,所以应该算作file处理?
                if item['playlist'].endswith('.tak'):
                    item['file'] = item['playlist']
                else:
                    open('/dev/shm/123', 'w').write(str(item))
                    print(item)
                    a = 1 / 0
    occupied = set(occupied)
    non_occupied = []
    for item in items:
        if 'file' in item:
            if item['file'] not in occupied:
                non_occupied.append(item)
    return non_occupied + playlists


def listall1(item, mpc):
    if 'directory' in item:
        return mpc.listallinfo(item['directory'])
    else:
        return [item]


def listall2(item, mpc, result=None):
    if None == result:
        result = []
    if 'directory' in item:
        try:
            uri = item['directory']
            if uri == '..':
                return []
            children = mpc.lsinfo(uri)
        except BaseException:
            # 可以强制加入utf8编码错误的文件，但是加入后，ncmpy的listview会出错，无法显示。
            children = mpc.listall(item['directory'])
            children = [item for item in children if 'file' in item]
        for child in children:
            listall2(child, mpc, result)
    else:
        logging.debug('add single item:%s', item)
        result.append(item)
    return result
