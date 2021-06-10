import threading
import cantools
import can
import pyaudio
import time
import sys

from receive_data import *

## These variables are used in receive_data.py to sync threads
TOTAL_THREADS_NUM = 4 ## Add 1 each time a sensor is added.
thread_count = 0

def main():
    print("Main thread started.")

    ### Audio setting ###
    FORMAT = pyaudio.paInt16
    RATE = 44100
    CHANNELS = 1
    CHUNK = 1024

    ### Thread setting ###
    stop_threads = False
    workers = []
    data_names = ['CAN', 'video', 'audio', 'sensor',]
    thread_functions = [receive_CAN, receive_video, receive_audio, receive_sensor,]
    func_args = {'CAN': (),
                 'video': (),
                 'audio': (FORMAT, RATE, CHANNELS, CHUNK),
                 'sensor': (),
                 }
    
    ### Thread generation ###
    print("Press 'Enter' if you want to terminate every processes.")
    for d_name, th_func in zip(data_names, thread_functions):
        worker = threading.Thread(target=th_func, args=(d_name, *func_args[d_name], lambda: stop_threads))
        workers.append(worker)
        worker.start()
    
    terminate_signal = input()
    while terminate_signal != '':
        print("Wrong input! Press 'Enter'")
        terminate_signal = input()
    stop_threads = True

    for worker in workers:
        worker.join()
    print("Main thread finished.")

    
if __name__ == "__main__":
    main()