from django.db import models

class CommitteeForm(models.Model):
    number = models.IntegerField(primary_key=True)
    request = models.ForeignKey("requests.Request", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey("requests.User", on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.number} - {self.request.number}"

class TechnicalForm(models.Model):
    number = models.IntegerField(primary_key=True)
    request = models.ForeignKey("requests.Request", on_delete=models.CASCADE)
    assigned_to = models.ForeignKey("requests.User", on_delete=models.CASCADE)
    details = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.number} - {self.request.number}"
