import jupyter_client
from sys import argv
import logging
from queue import Empty
import base64
from PIL import Image
#import time
#from  tempfile import TemporaryFile

def save_to_file(filename, data):
    file = open(filename, "wb")
    file.write(data)
    file.close()

def show_image(img_base64_data):
    img_binary_data = base64.b64decode(img_base64_data)
    img_name = "x.png"
    save_to_file(img_name, img_binary_data)
    img = Image.open(img_name)
    img.show()

def run_lines(lines, kernel, timeout=10, kernel_debug=True):
        msg_id = kernel.execute(lines)
        if kernel_debug:
            logging.debug("Executing lines (msg_id=%s):\n%s", msg_id, lines)
        # wait for finish, with timeout
        # At first we have to wait until the kernel tells us it is finished with running the code
        while True:
            try:
                msg = kernel.shell_channel.get_msg(timeout=timeout)
                if kernel_debug:
                    logging.debug("shell msg: %s", msg)
            except Empty:
                # This indicates that something bad happened, as AFAIK this should return...
                logging.error("Timeout waiting for execute reply")
                raise Exception("Timeout waiting for execute reply.")
            if msg['parent_header'].get('msg_id') == msg_id:
                # It's finished, and we got our reply, so next look at the results
                break
            else:
                # not our reply
                logging.warn("Discarding message from a different client: %s" % msg)
                continue

        # Now look at the results of our code execution and earlier completion requests
        # We handle messages until the kernel indicates it's ide again
        status_idle_again = False
        while True:
            try:
                msg = kernel.get_iopub_msg(timeout=timeout)
            except Empty:
                # There should be at least some messages: we just executed code!
                # The only valid time could be when the timeout happened too early (aka long
                # running code in the document) -> we handle that below
                logging.error("Timeout waiting for expected IOPub output")
                break

            if msg['parent_header'].get('msg_id') != msg_id:
                if msg['parent_header'].get(u'msg_type') != u'is_complete_request':
                    # not an output from our execution and not one of the complete_requests
                    logging.info("Discarding output from a different client: %s" % msg)
                else:
                    # complete_requests are ok
                    pass
                continue

            # Here we have some message which corresponds to our code execution
            msg_type = msg['msg_type']
            content = msg['content']

            # The kernel indicates some status: executing -> idle
            if msg_type == 'status':
                if content['execution_state'] == 'idle':
                    # When idle, the kernel has executed all input
                    status_idle_again = True
                    break
                else:
                    # the "starting execution" messages
                    continue
            elif msg_type == 'clear_output':
                # we don't handle that!?
                logging.debug("Discarding unexpected 'clear_output' message: %s" % msg)
                continue
            ## So, from here on we have a messages with real content
            if kernel_debug:
                logging.debug("iopub msg (%s): %s",msg_type, msg)
            ##print(msg)
            _handle_return_message(msg)

        if not status_idle_again:
            logging.info("Code lines didn't execute in time. Don't use long-running code in "
                           "documents or increase the timeout!")
            logging.info("line(s): %s" % lines)


def _handle_return_message(msg):
    if msg["msg_type"] == "display_data":
        img_base64_data = msg["content"]["data"]["image/png"]
        show_image(img_base64_data)
        print("<< " + msg["content"]["data"]["text/plain"])
    if msg["msg_type"] == "execute_input":
        print(">> " + msg["content"]["code"])
    if msg["msg_type"] == "error":
        print("<< " + "\n".join(msg["content"]["traceback"]))
    if msg["msg_type"] == "stream":
        print("<< " + msg["content"]["text"])

if __name__ == "__main__":


    kernel_manager, kernel_client = jupyter_client.manager.start_new_kernel(kernel_name='python3')
    commands = \
    [
        'import keras',
        'import matplotlib.pyplot as plt',
        'plt.plot([1, 2, 3, 4])',
        'plt.ylabel("some numbers")',
        'plt.show()',
        'a=5',
        'b=0',
        'print("hello there")',
        'print(a*10)',
#        'c=1/b'
    ]
    command = "\n".join(commands)   
#    for command in commands:
    run_lines(command, kernel_client)
    kernel_client.shutdown()
