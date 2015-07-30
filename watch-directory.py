import os
import sys
import time
import shutil
import logging
import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler


parser = argparse.ArgumentParser()
parser.add_argument('--input', dest = 'input', help = "Enter source directory to watch")
parser.add_argument('--output', dest = 'output', help = "Enter the directory to copy to")
args = parser.parse_args()

class ModifiedDirHandler(FileSystemEventHandler):
    def on_modified(self, event):
        filePath = event.src_path
        shutil.copy(filePath, os.path.abspath(args.output))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.path.abspath(args.input)
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