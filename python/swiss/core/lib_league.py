from typing import List, Set

from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.match import Match
from swiss.models.user import User


def create(user: User, title: str, win_mode: str) -> League:
    league = League()
    league.user = user
    league.title = title
    league.win_mode = win_mode;
    league.save()

    Player.objects.create(league=league, name='X', is_ghost=True)

    return league


def calculate_matches_result(matches: List[Match]) -> None:
    for match in matches:
        match.player1.initialize_results()
        match.player2.initialize_results()

    for match in matches:
        match.player1.matched.add(match.player2)
        match.player2.matched.add(match.player1)

        if match.score1 > match.score2:
            match.player1.increase_wins(match.player2)
            match.player2.increase_loses(match.player1)
        elif match.score2 > match.score1:
            match.player2.increase_wins(match.player1)
            match.player1.increase_loses(match.player2)
        else:
            match.player2.increase_draws()
            match.player1.increase_draws()

        if match.score1 == 2:
            match.player1.increase_score(7)
        elif match.score1 == 1:
            match.player1.increase_score(4)
            match.player2.increase_score(2)
        if match.score2 == 2:
            match.player2.increase_score(7)
        elif match.score2 == 1:
            match.player2.increase_score(4)
            match.player1.increase_score(2)
        if match.score1 == 0 and match.score2 == 0:
            match.player1.increase_score(3)
            match.player2.increase_score(3)


def calculate_rankings(players: Set[Player], matches: Set[Match]) -> None:
    for m_player in players:
        m_player.initialize_ranking()
        m_player.buchholz = sum([opponent.wins * League.win_score + opponent.draws for opponent in m_player.matched])

    # dict_players_by_first
    dict_players_by_first = {}
    for m_player in players:
        first_value = m_player.get_ranking_first()
        if first_value not in dict_players_by_first:
            dict_players_by_first[first_value] = set()
        dict_players_by_first[first_value].add(m_player)

    # calculate all kill
    for first_value, the_players in dict_players_by_first.items():
        if len(the_players) <= 1:
            continue

        ak_players = set(the_players)

        while len(ak_players) > 1:
            for m_player in ak_players:
                m_player.all_kill = 0

            w_matches = (m for m in matches if (m.player1 in ak_players and m.player2 in ak_players))
            for m_match in w_matches:
                if m_match.score1 > m_match.score2:
                    m_match.player1.all_kill += 1
                elif m_match.score2 > m_match.score1:
                    m_match.player2.all_kill += 1

            found_all_kill = False
            next_ak_players = set()
            for m_player in ak_players:
                if m_player.all_kill == len(ak_players) - 1:
                    found_all_kill = True
                else:
                    m_player.all_kill = 0
                    next_ak_players.add(m_player)

            if found_all_kill:
                ak_players = next_ak_players
            else:
                break

    sorted_players = sorted(players,
                            key=lambda p: p.get_ranking_first() + (p.all_kill,) + p.get_ranking_second(),
                            reverse=True)
    for idx, m_player in enumerate(sorted_players):
        m_player.ranking = idx+1
