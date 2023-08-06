import threading
import time
from signal import SIGINT, SIGTERM, signal

from agents import Agent, Message

# generate public and private keys for server and client
server_public_key, server_private_key = Agent.curve_keypair()
wrong_server_public_key, wrong_server_private_key = Agent.curve_keypair()
client_public_key, client_private_key = Agent.curve_keypair()
client2_public_key, client2_private_key = Agent.curve_keypair()


class NotificationBroker(Agent):
    def setup(self, name=None, pub_address=None, sub_address=None):
        self.create_notification_broker(
            pub_address,
            sub_address,
            options=self.curve_server_config(server_private_key),
        )


class Sender(Agent):
    def setup(self, name=None, pub_address=None, sub_address=None):
        self.counter = 0
        self.pub, self.sub = self.create_notification_client(
            pub_address,
            sub_address,
            options=self.curve_client_config(
                server_public_key, client_public_key, client_private_key
            ),
        )

        # begin sending forever, add to managed threads for graceful cleanup
        t = threading.Thread(target=self.send_forever)
        self.threads.append(t)
        t.start()

    def send_forever(self):
        # use exit event to gracefully exit loop and graceful cleanup
        while not self.exit_event.is_set():
            time.sleep(1)
            self.counter += 1
            msg = Message.Notification(payload=str(self.counter))
            self.log.info(f"publishing: {msg}")
            self.pub.send(msg.to_multipart())


class Listener(Agent):
    def setup(self, name=None, pub_address=None, sub_address=None):
        self.pub, self.sub = self.create_notification_client(
            pub_address,
            sub_address,
            options=self.curve_client_config(
                server_public_key, client_public_key, client_private_key
            ),
        )
        self.sub.observable.subscribe(lambda x: self.log.info(f"received: {x}"))


class ListenerInvalid(Agent):
    def setup(self, name=None, pub_address=None, sub_address=None):
        self.pub, self.sub = self.create_notification_client(
            pub_address,
            sub_address,
            options=self.curve_client_config(
                wrong_server_public_key, client2_public_key, client2_private_key
            ),
        )
        self.sub.observable.subscribe(lambda x: self.log.info(f"received: {x}"))


if __name__ == "__main__":
    broker = NotificationBroker(
        name="broker",
        pub_address="tcp://0.0.0.0:5000",
        sub_address="tcp://0.0.0.0:5001",
    )
    sender = Sender(
        name="sender",
        pub_address="tcp://0.0.0.0:5000",
        sub_address="tcp://0.0.0.0:5001",
    )
    listener = Listener(
        name="listener",
        pub_address="tcp://0.0.0.0:5000",
        sub_address="tcp://0.0.0.0:5001",
    )
    listener_invalid = ListenerInvalid(
        name="listener_invalid",
        pub_address="tcp://0.0.0.0:5000",
        sub_address="tcp://0.0.0.0:5001",
    )

    # override shutdown signals
    def shutdown(signum, frame):
        listener.shutdown()
        listener_invalid.shutdown()
        sender.shutdown()
        broker.shutdown()

    signal(SIGTERM, shutdown)
    signal(SIGINT, shutdown)
