import gzip
import os
import pickle
import queue
import threading

from domains import Course, Student

DATA_FILE = "students.dat"

_save_queue = queue.Queue()


def _snapshot(manager):
    return {
        "courses": {c.cid: (c.name, c.credits) for c in manager.courses.values()},
        "students": {
            s.sid: (s.name, s.dob, dict(s.marks)) for s in manager.students.values()
        },
    }


def _worker():
    while True:
        data = _save_queue.get()
        try:
            if data is None:  # shutdown signal
                return
            tmp = DATA_FILE + ".tmp"
            with gzip.open(tmp, "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
            os.replace(tmp, DATA_FILE)
        finally:
            _save_queue.task_done()


_thread = threading.Thread(target=_worker, daemon=True)
_thread.start()


def save_data(manager):
    # Queues a save
    _save_queue.put(_snapshot(manager))


def compress_data():
    # Wait for pending saves, then stop the worker
    _save_queue.join()
    _save_queue.put(None)
    _thread.join()


def load_data(manager):
    if not os.path.exists(DATA_FILE):
        return
    with gzip.open(DATA_FILE, "rb") as f:
        data = pickle.load(f)
    for cid, (name, credits) in data["courses"].items():
        manager.courses[cid] = Course(cid, name, credits)
    for sid, (name, dob, marks) in data["students"].items():
        student = Student(sid, name, dob)
        student.marks.update(marks)
        manager.students[sid] = student
