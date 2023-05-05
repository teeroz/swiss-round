from django.db import models

from swiss.models.league import League


class Round(models.Model):
    league = models.ForeignKey(League, related_name='rounds', on_delete=models.CASCADE)
    no = models.PositiveSmallIntegerField()
    tournament_stage = models.PositiveSmallIntegerField(default=0)
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return '{} round'.format(self.no)
