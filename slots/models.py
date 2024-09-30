from django.db import models

class Slot(models.Model):
    link = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.link} - {'Active' if self.is_active else 'Used'}"
