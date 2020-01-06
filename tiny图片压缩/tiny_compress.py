import tinify
import os
import threading
import queue
import time

#tinify申请key,每月免费500张
tinify.key = 'XfY8wwyBx9Vb2kJMtFw9YSYHshdzt8DX'
lock = threading.Lock()
#剩余任务
urlList = []

#单线程
def compress(path):
    if os.path.isdir(path):
        for root,dirs,files in os.walk(path):
            for file in files:
                if file.endswith(('jpg','JPG','png','PNG')):
                    p = os.path.join(root,file)
                    print('compress......'+p)
                    source = tinify.from_file(p)
                    source.to_file(p)
                pass
            pass
        pass
    elif os.path.isfile(path):
        print('compress......'+path)
        source = tinify.from_file(path)
        source.to_file(path)
        pass
    else:
        print("路径无效")
        return

def getImagePath(path):
    paths = queue.Queue()
    if os.path.isdir(path):
        for root,dirs,files in os.walk(path):
            for file in files:
                if file.endswith(('jpg','JPG','png','PNG')):
                    p = os.path.join(root,file)
                    paths.put(p)
                    urlList.append(p)
                pass
            pass
        pass
    elif os.path.isfile(path):
        paths.put(p)
        urlList.append(p)
        pass
    else:
        print("\033[0;31;40m路径无效\033[0m")
    return paths

def compressThread(queuePaths,name):
    while not queuePaths.empty():
        try:
            p = queuePaths.get(False)
            size = queuePaths.qsize()
            source = tinify.from_file(p)
            source.to_file(p)
            lock.acquire()
            urlList.remove(p)
            lock.release()
            print("compress......%s" % p)
            pass
        except expression as identifier:
            pass
    print('thread%d....end...' % name)
    pass

def main():
    params = input('输入路径：').split(" ")
    if len(params) > 1 and params[1]:
        tinify.key = params[1]

    #多线程
    queuePaths = getImagePath(params[0])
    size = queuePaths.qsize()
    print("图片总数："+str(size))
    threads = []
    threadCount = 20
    if queuePaths and queuePaths.qsize() > 1:
        for i in range(threadCount):
            t = threading.Thread(target=compressThread,args=(queuePaths,i,))
            t.setDaemon(True)
            threads.append(t)
        for t in threads:
            t.start()
            pass
    else:
        return
        pass

    #这里主线程等待时间为timeout * threadCount
    for t in threads:
        t.join(10)
        pass
    

    #单线程
    # compress(params[0])


    for url in urlList:
        print("\033[0;31;40m未完成：%s\033[0m" % url)
        pass
    print("压缩进度：%d/%d" % (size-len(urlList),size))

    if tinify.compression_count:
        print("\033[0;32;40m剩余张数：%d/500\033[0m" % tinify.compression_count)

    input("任意键退出")

if __name__ == "__main__":
    main()
    