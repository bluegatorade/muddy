import backend_server
import manager
from threading import Thread

if __name__ == "__main__":
    Thread(target=backend_server.Start).start()
    Thread(target=manager.Start).start()