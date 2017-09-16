from django.dispatch import Signal

digest_event = Signal(providing_args=["user", "title", "link", "duration"])
