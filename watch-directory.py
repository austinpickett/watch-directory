import os
import sys
import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler

class ModifiedDirHandler(FileSystemEventHandler):
    def on_modified(self, event):
        filePath = event.src_path
        shutil.copy(filePath, os.path.abspath(".."))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.path.abspath('.')
    event_handler = ModifiedDirHandler()
    observer = Observer()
    observer.schedule(LoggingEventHandler(), path, recursive=True)
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    import sys