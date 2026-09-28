"""
this is the message recver this thing allows me to see all the messages on all the ports

TODO: get everything orgizied better

"""



import zmq
from colorama import Fore, Back, Style

context = zmq.Context()

controller = context.socket(zmq.SUB)

recv = context.socket(zmq.SUB)


controller.connect("tcp://" + "127.0.0.1:5001")
recv.connect("tcp://" + "127.0.0.1:5002")

recv.setsockopt(zmq.SUBSCRIBE,b"")
controller.setsockopt(zmq.SUBSCRIBE,b"")

poller = zmq.Poller()
poller.register(controller, zmq.POLLIN)


print(Fore.LIGHTGREEN_EX + f"Starting Zmq Pipeline Monitor...")
while True:

    evts = dict(poller.poll(timeout=100))




    if recv in evts:

        topic = recv.recv_string()
        status = recv.recv_json()
        
        print(topic + " "+ "from port 5002")

        if topic == "PIPELINE":
            print(Fore.YELLOW + f"Topic: {topic} => {status}")
            print(Fore.RESET)

        if topic == "TEXTMESSAGES":
            print(Fore.LIGHTMAGENTA_EX + f"Topic: {topic} => {status}")
            print(Fore.RESET)

        if topic == "ERROR":
            print(Fore.RED + f"Topic: {topic} => {status}")
            print(Fore.RESET)

        if topic == "LIVENESS_STATS":
            print(Fore.CYAN + f"Topic: {topic} => {status}")
            print(Fore.RESET)


        if topic == "SENSOR":
            print(Fore.GREEN + f"Topic: {topic} => {status}")
            print(Fore.RESET)


    if controller in evts:

        topic = controller.recv_string()
        status = controller.recv_json()

        print(topic + " "+ "from port 5001")

        if topic == "PIPELINE":
            print(Fore.YELLOW + f"Topic: {topic} => {status}")
            print(Fore.RESET)

        if topic == "USERS":
            print(Fore.GREEN + f"Topic: {topic} => {status}")
            print(Fore.RESET)

        if topic == "ERROR":
            print(Fore.RED + f"Topic: {topic} => {status}")
            print(Fore.RESET)

        if topic == "LIVENESS":
            print(Fore.CYAN + f"Topic: {topic} => {status}")
            print(Fore.RESET)
