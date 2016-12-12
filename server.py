import snakemq.link
import snakemq.packeter
import snakemq.messaging
import snakemq.message

# global defines
SERVER_IDENT = "server"

server_link = snakemq.link.Link()
server_packeter = snakemq.packeter.Packeter(server_link)
server_messaging = snakemq.messaging.Messaging(SERVER_IDENT, "", server_packeter)

server_link.add_listener(("", 4000))  # listen on all interfaces and on port 4000

client_idents = list()
# add message parser
def on_recv(conn, ident, message):
    print "new message from %s : %s" % (ident, message.data)
    message = snakemq.message.Message(b"ack", ttl=600)
    server_messaging.send_message(ident, message)

server_messaging.on_message_recv.add(on_recv)

# add connection manager to deal out unique idents
def on_conn(conn_id):
	print "new connection: %s" % conn_id
	server_packeter.send_packet(conn_id, "ASSIGN ID:"+str(conn_id))
	client_idents

server_packeter.on_connect.add(on_conn)


def main_loop():
	return

server_link.on_loop_pass.add(main_loop)

server_link.loop()

