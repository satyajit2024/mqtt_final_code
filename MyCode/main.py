from mqtt import MqttConnect
import threading

mq = MqttConnect()
if __name__ == '__main__':
    t1 = threading.Thread(target=mq.post_data_to_publish)
    t2 = threading.Thread(target=mq.data_subscribe)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("| Done |")
