import threading
import time


def doingjop(_jobs, _delay, _name):

    print(f"{_name} 님에게 {_jobs}개의 일이 주어졌습니다.\n")

    for i in range(_jobs):
        print(f"{_name} 님이 {i+1}번 째 일을 완료하였습니다.\n")
        time.sleep(_delay)

    print(f"{_name} 님이 일을 마치고 퇴근합니다.\n")


thread_1 = threading.Thread(target= doingjop, args = (5, 0.1, ' 일반 직원'))
thread_1.start()

thread_2 = threading.Thread(target= doingjop, args = (10, 0.1, '  관리 직원'))
thread_2.daemon = True
thread_2.start()

doingjop(3, 0.1, '사장')
