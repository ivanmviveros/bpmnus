from django.db import models


from projects.models import Projects
# Create your models here.

class Diagrams(models.Model):
    """Model to represent a diagram"""
    project = models.ForeignKey(Projects, on_delete=models.DO_NOTHING)
    name = models.TextField()
    desc = models.TextField()
    xml = models.TextField()
    propierties = models.TextField()
    creation_date = models.DateTimeField()


class UserStory(models.Model):
    diagram = models.ForeignKey(Diagrams, on_delete=models.CASCADE, related_name="user_stories")
    data = models.JSONField()

    def get_html(self):
        from diagrams.business_logic.transform_xml import generate_us_html
        return generate_us_html(self.data)
