import paho.mqtt.client as mqtt
import logging
import time
import sys
import os

os.system('cls')
broker = "broker.hivemq.com"
logging.basicConfig(filename="MQTT.log",
                    filemode="w",
                    level=logging.INFO)


def on_log(client, userdata, level, buf):
    logging.info(f"Log: {buf}")
    print('Log: ' + buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected With Return Code {rc}")
        logging.info(f"Connected OK, Return Code: {rc}")
        client.connected_flag = True  # set Flag
    else:
        conn_code = {1: "Connection refused – incorrect protocol version",
                     2: "Connection refused – invalid client identifier",
                     3: "Connection refused – server unavailable",
                     4: "Connection refused – bad username or password",
                     5: "Connection refused – not authorised"}
        print(conn_code.get(rc))
        logging.info(conn_code.get(rc))
        client.bad_connection_flag = True


def on_disconnect(client, userdata, flags, rc=0):
    logging.info(f"Disconnected, Result Code {rc}")
    print(f"Disconnected, Result Code {rc}")
    client.connected_flag = False
    client.disconnect_flag = True
    client.loop_stop()


def on_publish(client, userdata, mid):
    logging.info(f"In Publish Callback Function, Mid = {mid}")


def on_message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8"))
    logging.info(f"Message Recieved:- '{m_decode}' ")
    print(f"Message Recieved:- '{m_decode}' ")


def on_sunscribe(client, userdata, mid, granted_qos):
    logging.info(f"Subscribed {mid}")


# Connection Flags
mqtt.Client.connected_flag = False

# Create new instance of the Class
client = mqtt.Client("program1", clean_session=False)
time.sleep(1)

# Binding the Call back Function
client.on_log = on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message = on_message
client.on_sunscribe = on_sunscribe

topics = [("PideParker/Tokens", 0),
          ("PideParker/Tokens", 1),
          ("PideParker/Tokens", 2)]
topic_ack = []

try:
    client.connect(broker)  # Connecting To the broker
    client.loop_start()  # Start Loop

except ConnectionRefusedError as cre:
    logging.critical(f"Broker Server is not running {broker}")
    sys.exit("ConnectionRefusedError, Exiting!!")

# Raises For Bad IP, Socket Error, and Port Number
except TimeoutError as toe:
    logging.critical(f"Broker Server Not Responding {broker}")
    sys.exit("TimeoutError, Exiting!!")


except KeyboardInterrupt as ki:
    logging.error("Quitting on Users Choice...")
    sys.exit("Quitting")

else:
    # Handling Bad Connection Faliure
    while not client.connected_flag:  # wait in loop
        print("In the waiting Loop\n")
        time.sleep(1)

# Subscribing To PideParker Topic
logging.debug(f"Subscribing {str(topics)}")
for t in topics:
    try:
        r = client.subscribe(t)
        if r[0] == 0:
            logging.info(f"Subscribed To Topic: {str(t[0])}")
            topic_ack.append([t[0], r[1], 0])  # Keeping Track of Subscription
        else:
            logging.error(f"Error on Subscribing {str(r)}")
            client.loop_stop()  # Stop Loop on Error
    except Exception as e:
        logging.critical(f"Error on Subscribing {str(r)}")
        client.loop_stop()  # Stop Loop on error
        sys.exit("Subscribing Error!! Quitting")

logging.info("Publishing the Message")

# Publish QoS 0
ret = client.publish("PideParker/Tokens", "Test Message 0", 0)
logging.info(f"Published return = {ret}")
time.sleep(3)

# Publish QoS 1
ret = client.publish("PideParker/Tokens", "Test Message 1", 1)
logging.info(f"Published return = {ret}")
time.sleep(3)

# Publish QoS 2
ret = client.publish("PideParker/Tokens", "Test Message 2", 2)
logging.info(f"Published return = {ret}")
time.sleep(3)


time.sleep(1)
client.loop_stop(1)  # Stop Loop
client.disconnect()  # Disconnect