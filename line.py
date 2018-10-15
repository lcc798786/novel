import get_novel
import threading

for i in range(5):
    n=threading.Thread(target=get_novel.url.get_novel(),args=(i,))
    n.start()

