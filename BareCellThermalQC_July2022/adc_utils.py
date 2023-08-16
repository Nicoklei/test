import socket
import pickle
import logging
import time

def query(tcp_socket, HEADERSIZE):
    try:
        message_header = tcp_socket.recv(HEADERSIZE)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return True
    except:
        return False

def receive(tcp_socket, HEADERSIZE):
    full_msg = b''
    loop_timeout = time.time() + 20
    #logging.info("keine Ahnung")
    while True:
        if time.time() > loop_timeout:
            break
        try:
            msg = tcp_socket.recv(48000)
            # logging.info("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            # logging.info(f"full message length: {msglen}")
            full_msg =  msg
            # logging.info(len(full_msg))
            if len(full_msg)-HEADERSIZE == msglen:
                # logging.info(full_msg[HEADERSIZE:])
                data = pickle.loads(full_msg[HEADERSIZE:])
                full_msg = b""
                # logging.info(f"received data:{data}")
                return data
        except socket.timeout:
            print("socket timed out")
            tcp_socket.close()
        except Exception as e:
            logging.info(e)
            break

def send(tcp_socket, HEADERSIZE, data):
    try:
        msg = pickle.dumps(data)
        msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
        tcp_socket.send(msg)
    except Exception as e:
        logging.info(e)