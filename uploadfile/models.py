from django.db import models
import hashlib


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """ذخیره رمز عبور به صورت هش‌شده"""
        self.password = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password):
        """بررسی صحت رمز عبور"""
        return self.password == hashlib.sha256(raw_password.encode()).hexdigest()


class File(models.Model):
    format = models.CharField(max_length=50)
    file_name = models.CharField(max_length=255)
    file_address = models.FileField(upload_to='uploads/')
    file_size = models.PositiveIntegerField()
    title = models.CharField(max_length=255, blank=True)
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_files', null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_files', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or self.file_name
