#!/usr/bin/env python
#benchmark.py

import zmq
from time import time


def action(command, object_id):
    # TODO implement the RAWX action and return the HTTP code
    return 501


def worker(zctx, endpoints):
    zcmd = zctx.socket(zmq.REP)
    # zcmd.set_hwm(512)
    for endpoint in endpoints:
        zcmd.connect(endpoint)
    try:
        while True:
            message = zcmd.recv_string()
            action_id, command, object_id = message.split()
            pre = time()
            rc = action(command, object_id)
            post = time()
            zcmd.send_string("%s %d %0.6f" % (action_id, rc, post - pre))
    except KeyboardInterrupt:
        pass
    zcmd.close()


def controller(zctx, endpoints):
    zcmd = zctx.socket(zmq.DEALER)
    # zcmd.set_hwm(512)
    for endpoint in endpoints:
        zcmd.bind(endpoint)
    try:
        reqid = 0
        while True:
            events = zcmd.poll(timeout=1000, flags=zmq.POLLIN | zmq.POLLOUT)
            if events & zmq.POLLIN:
                zcmd.recv()
                reply = zcmd.recv_string()
                print reply
            if events & zmq.POLLOUT:
                # TODO implement a ramp up
                cmd = ('PUT', 'GET', 'DELETE')
                obj = "0123456789BACDEF" * 4
                action = cmd[reqid % 3]
                zcmd.send("", flags=zmq.SNDMORE)
                zcmd.send_string("{0} {1} {2}".format(reqid, action, obj))
                reqid += 1
    except KeyboardInterrupt:
        pass
    zcmd.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Benchmark tool")
    parser.add_argument("--worker",
                        dest="worker", action='store_true', default=False,
                        help='Start a worker connecter to the given addresses')
    parser.add_argument("--controller",
                        dest="controller", action='store_true', default=False,
                        help='Start a controller bond to the given addresses')
    parser.add_argument("endpoints",
                        metavar='ENDPOINT', type=str, nargs='+',
                        help='Endpoints to connect/bind to')
    args = parser.parse_args()

    zctx = zmq.Context()
    if args.controller:
        controller(zctx, args.endpoints)
    elif args.worker:
        worker(zctx, args.endpoints)
    else:
        parser.print_help()
    zctx.term()