from django.db import models
from django.forms import model_to_dict

from swiss.models.league import League


class Player(models.Model):
    league = models.ForeignKey(League, related_name='players', on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    memo = models.CharField(max_length=64, default='')
    is_ghost = models.BooleanField(default=False)
    is_dropped = models.BooleanField(default=False)
    is_family = models.BooleanField(default=False)
    family = models.ManyToManyField("self", symmetrical=True, blank=True)
    create_dt = models.DateTimeField(auto_now_add=True)
    modify_dt = models.DateTimeField(auto_now=True)

    wins = 0
    draws = 0
    loses = 0
    strikes_count = 0
    strikes_start = 0
    max_strikes_count = 0
    max_strikes_start = 0
    score = 0

    matched = set()
    matched_wins = set()
    matched_loses = set()
    matched_same = set()
    matched_lower = set()

    # 상대의 승점을 합한 점수
    buchholz = 0
    # 승자승 결정을 위한 변수
    all_kill = 0

    ranking = 0

    def __str__(self) -> str:
        return str(self.name)

    def initialize_results(self) -> None:
        self.wins = 0
        self.half_wins = 0
        self.draws = 0
        self.loses = 0
        self.half_loses = 0
        self.strikes_count = 0
        self.strikes_start = 0
        self.max_strikes_count = 0
        self.max_strikes_start = 0
        self.matched = set()
        self.matched_wins = set()
        self.matched_loses = set()
        self.score = 0

    def increase_wins(self, opponent) -> None:
        self.wins += 1
        if self.strikes_count <= 0:
            self.strikes_start = self.wins + self.draws + self.loses
        self.strikes_count += 1
        if self.strikes_count > self.max_strikes_count:
            self.max_strikes_start = self.strikes_start
            self.max_strikes_count = self.strikes_count

        self.matched_wins.add(opponent)

    def increase_half_wins(self) -> None:
        self.half_wins += 1

    def increase_draws(self) -> None:
        self.draws += 1
        self.strikes_count = 0

    def increase_loses(self, opponent) -> None:
        self.loses += 1
        self.strikes_count = 0

        self.matched_loses.add(opponent)

    def increase_half_loses(self) -> None:
        self.half_loses += 1

    def increase_score(self, score) -> None:
        self.score += score

    def initialize_ranking(self) -> None:
        self.buchholz = 0
        self.ranking = 0

    def get_ranking_first(self, league: League) -> tuple:
        if league.ranking_criteria == 'winner':
            return not self.is_ghost, self.score
        else:
            return not self.is_ghost, self.score, self.buchholz

    def get_ranking_second(self, league: League) -> tuple:
        if league.ranking_criteria == 'winner':
            return self.buchholz, self.max_strikes_count, self.max_strikes_start * -1
        else:
            return self.max_strikes_count, self.max_strikes_start * -1

    def to_dict(self) -> dict:
        to_dict = model_to_dict(self, exclude="family")
        to_dict.update({
            'wins': self.wins,
            'half_wins': self.half_wins,
            'draws': self.draws,
            'loses': self.loses,
            'half_loses': self.half_loses,
            'max_strikes_count': self.max_strikes_count,
            'max_strikes_start': self.max_strikes_start,
            'buchholz': self.buchholz,
            'all_kill': self.all_kill,
            'ranking': self.ranking,
            'score': self.score
        })

        return to_dict
