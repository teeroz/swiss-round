from typing import Optional, List

from swiss.core import lib_league
from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.round import Round
from swiss.models.match import Match


def start_new_tournament(m_league: League, stage: int) -> Optional[Round]:
    new_matches = _get_matches_of_new_tournament(m_league, stage)  # type: List[(Player, Player)]
    if new_matches is None:
        return None

    m_round = Round.objects.create(league=m_league, no=1, tournament_stage=stage)

    for player1, player2 in new_matches:
        Match.objects.create(league=m_league, round=m_round, player1=player1, player2=player2)

    return m_round


def _get_matches_of_new_tournament(m_league: League, stage: int) -> Optional[list]:
    players = lib_league.get_players_order_by_ranking(m_league)[:stage]  # type: List[Player]

    matched_players = []
    for i in range(0, stage):
        t = i  # type: int
        s = stage  # type: int
        d = 1   # type: int
        while True:
            if t == 0:
                matched_players.append(players[0])
                break

            if t % 2 == 1:
                opponent = matched_players[(t - 1) * d]
                matched_players.append(players[s - opponent.ranking])
                break

            t = int(t / 2)
            s = int(s / 2)
            d = int(d * 2)

    result = []
    for i in range(0, int(stage / 2)):
        result.append((matched_players[i*2], matched_players[i*2+1]))

    return []
