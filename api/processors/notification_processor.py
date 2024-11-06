import threading
# Threading allows to use background timers to repeatedly call a function

NOTIFICATION_UPDATE_INTERVAL_SEC = 30
# Sets the interval at which notifications are sent.
# It sends notifications every 30 seconds

_queue = ["Dummy message"]
# This is a queue with notifications in it


def push(notification):
    # This function receives a notification as a parameter
    global _queue
    _queue.append(notification)
    # It adds the notification to the queue


def send():
    # Check if the queue contains any notifications
    if len(_queue) > 0:
        notification = _queue.pop(0)
        # It removes the first notification in the queue
        # and assigns it to the variable 'notification'
        print(notification)
        # It the notification that was popped
    threading.Timer(NOTIFICATION_UPDATE_INTERVAL_SEC, send).start()
    # Sets a timer to call 'send()' again after the specified interval,
    # which is 30 seconds

    # It creates a timer and tells the timer to countdown,
    # before calling the function again.

    # After 30 seconds 'send()' is called again


def start():
    # Calls 'send()'
    send()
