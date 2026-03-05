"""Piko holder for managing updates."""
import time

from kostalpiko.kostalpiko import Piko


class PikoHolder(Piko):
    """Piko holder class."""

    last_update = 0
    update_running = False

    def __init__(self, host=None, username="pvserver", password="pvwr") -> None:
        """Initialize PikoHolder."""
        super().__init__(host, username, password)

    def update(self):
        """Update data with throttling."""
        if not self.update_running:
            if time.time() - self.last_update > 30.0:
                self.update_running = True
                self.last_update = time.time()
                super().update()
                self.update_running = False
