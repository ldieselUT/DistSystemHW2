import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message

import threading

CLIENT_IDENT = "client"

client_link = snakemq.link.Link()
client_packeter = snakemq.packeter.Packeter(client_link)
client_messaging = snakemq.messaging.Messaging(CLIENT_IDENT, "", client_packeter)

client_link.add_connector(("localhost", 4000))
client_link.add_connector(("localhost", 4001))

# drop after 600 seconds if the message can't be delivered
message = snakemq.message.Message(b"hello", ttl=600)
client_messaging.send_message("server", message)


i = 0

# handle messages recieved
def on_recv(conn, ident, message):
    print ident, message.data

client_messaging.on_message_recv.add(on_recv)

# handle setting up unique idents because snakeMQ does not support duplicate idents
def on_packet(conn_id, packet):
	global CLIENT_IDENT, client_messaging
	if "ASSIGN ID:" in packet:
		CLIENT_IDENT = packet.split(":")[1]
		print "new ident: ", CLIENT_IDENT
		client_messaging = snakemq.messaging.Messaging(CLIENT_IDENT, "", client_packeter)

client_packeter.on_packet_recv.add(on_packet)


def main_loop():
	global message, i
	client_messaging.send_message("server", message)
	message = snakemq.message.Message(b"hello" + str(i), ttl=600)
	i += 1


client_link.on_loop_pass.add(main_loop)
client_link.loop()

