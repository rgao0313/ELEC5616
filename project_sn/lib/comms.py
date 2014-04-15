import struct

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from dh import create_dh_key, calculate_dh_secret

class StealthConn(object):
    def __init__(self, conn, client=False, server=False, verbose=False, rsaKey=False):
        self.conn = conn
        self.cipher = None
        self.client = client
        self.server = server
        self.verbose = verbose
        self.rsaKey = rsaKey
        self.initiate_session()

    def initiate_session(self):
        # Perform the initial connection handshake for agreeing on a shared secret
        if not self.rsaKey:
            return

        ### TODO: Your code here!
        # This can be broken into code run just on the server or just on the client
        if self.server:
            my_public_key, my_private_key = create_dh_key()
            # Send them our public key
            self.send(bytes(str(my_public_key), "ascii"))
            # Receive encrypted iv with dh public key
            encrypted_data = self.recv()
            decrypted_data = self.rsaKey.decrypt(encrypted_data).split(
            # Obtain our shared secret
            shared_hash = calculate_dh_secret(their_public_key, my_private_key)
        if self.client:
            self.iv = Random.new().read(AES.block_size)
            # dh init
            my_public_key, my_private_key = create_dh_key()
            # 

        print("Shared hash: {}".format(shared_hash))
        # AES
        self.cipher = AES.new(shared_hash, AES.MODE_CBC, self.iv);

    def send(self, data):
        if self.cipher:
            encrypted_data = self.cipher.encrypt(data)
            if self.verbose:
                print("Original data: {}".format(data))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Sending packet of length {}".format(len(encrypted_data)))
        else:
            encrypted_data = data

        # Encode the data's length into an unsigned two byte int ('H')
        pkt_len = struct.pack('H', len(encrypted_data))
        self.conn.sendall(pkt_len)
        self.conn.sendall(encrypted_data)

    def recv(self):
        # Decode the data's length from an unsigned two byte int ('H')
        pkt_len_packed = self.conn.recv(struct.calcsize('H'))
        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]

        encrypted_data = self.conn.recv(pkt_len)
        if self.cipher:
            data = self.cipher.decrypt(encrypted_data)
            if self.verbose:
                print("Receiving packet of length {}".format(pkt_len))
                print("Encrypted data: {}".format(repr(encrypted_data)))
                print("Original data: {}".format(data))
        else:
            data = encrypted_data

        return data

    def close(self):
        self.conn.close()
