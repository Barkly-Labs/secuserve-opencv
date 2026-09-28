"""
This class is for running my video pipeline 
TODO: add code to launc from zmq
"""


from zmq.sugar import constants, poll
from pipeline import pipelineStates
from util import const

from util import consoleLog
import zmq

import imagezmq

from zmq import asyncio

context = zmq.Context(io_threads=4)
asyncContext = zmq.Context(io_threads=4)

# inits Sender and reciver Sockets for the Module
sender = context.socket(zmq.PUB)
receiver = context.socket(zmq.SUB)
receiver.setsockopt(zmq.SUBSCRIBE,b"")

imagesocket = None

poller = zmq.Poller()
poller.register(receiver, zmq.POLLIN)


def main():
    watchdog = 0

    consoleLog.Warning("Initing zmq")


    sender.bind(const.zmq_send)
    receiver.connect(const.zmq_recv)

    imagesocket = imagezmq.ImageSender(connect_to="tcp://127.0.0.1:5555", REQ_REP=False)

    consoleLog.PipeLine_Ok("running zmq")
    consoleLog.Warning("running VideoProcessing Pipeline...")



    # sets pipeline starting state so Fsm has all needed to run
    pipe = pipelineStates.PipeLine()
    pipe.on_event(pipelineStates.States.SETUP_PIPELINE, sender,receiver,poller,imagesocket)
    pipe.on_event(pipelineStates.States.TRAIN_MODEL, sender,receiver,poller,imagesocket)
    pipe.on_event(pipelineStates.States.RUN_RECONITION, sender,receiver,poller,imagesocket)


if __name__ == "__main__":
    main()
