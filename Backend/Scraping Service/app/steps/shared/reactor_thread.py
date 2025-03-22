from threading import Thread
from twisted.internet import reactor

from app.utils.logger import info, err


class ReactorThread:

    def __init__(self):
        self.reactor_thread = None

    def start(self):
        """Start the Twisted reactor in a separate thread."""
        try:
            if not reactor.running:
                self.reactor_thread = Thread(target=reactor.run, args=(False,))
                self.reactor_thread.start()
                info("Twisted reactor started.")
        except Exception as e:
            err(f"Failed to start reactor: {e}")

    def stop(self):
        """Stop the Twisted reactor."""
        try:
            if reactor.running:
                reactor.stop()
                self.reactor_thread.join()
                self.reactor_thread = None
                info("Twisted reactor stopped.")
        except Exception as e:
            err(f"Failed to stop reactor: {e}")


reactor_thread = ReactorThread()
