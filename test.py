import time
import asyncio
import threading

from signal import SIGINT, SIGTERM

async def fun():
	i = 0
	try:
		for i in range(5):
			try:
				i = i+ 2
				print(i)
				await asyncio.sleep(2)
			except KeyboardInterrupt:
				print('interrupted!')
	except KeyboardInterrupt:
	    print('interrupted!')

async def fun2():
	i = 0
	try:
		for i in range(5):
			try:
				i = i+ 3
				print(i)
				await asyncio.sleep(3)
			except KeyboardInterrupt:
				print('interrupted!')
	except KeyboardInterrupt:
	    print('interrupted!')

def thr(i):
	# we need to create a new loop for the thread, and set it as the 'default'
	# loop that will be returned by calls to asyncio.get_event_loop() from this
	# thread.
	loop = asyncio.new_event_loop()	
	asyncio.set_event_loop(loop)
	
	try:
		if (i == 1):
			fun1 = asyncio.ensure_future(fun())
			loop.add_signal_handler(SIGINT, fun1.cancel)
			loop.add_signal_handler(SIGTERM, fun1.cancel)
			loop.run_until_complete(fun1)
		else:
			fun_2 = asyncio.ensure_future(fun2())
			loop.add_signal_handler(SIGINT, fun_2.cancel)
			loop.add_signal_handler(SIGTERM, fun_2.cancel)
			loop.run_until_complete(fun_2)  
		
	finally:
		loop.close()

def main():
	num_threads = 2
	threads = [ threading.Thread(target = thr, args=(i,)) for i in range(num_threads) ]
	[ t.start() for t in threads ]
	[ t.join() for t in threads ]
	print("bye")

if __name__ == "__main__":
	main()