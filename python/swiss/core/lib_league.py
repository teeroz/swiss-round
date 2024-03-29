from typing import List

from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.match import Match
from swiss.models.user import User


def create(user: User, title: str, win_mode: str, ranking_criteria: str) -> League:
    league = League()
    league.user = user
    league.title = title
    league.win_mode = win_mode
    league.ranking_criteria = ranking_criteria
    league.save()

    Player.objects.create(league=league, name='X', is_ghost=True)

    return league


def calculate_matches_result(m_league: League, matches: List[Match]) -> None:
    for match in matches:
        match.player1.initialize_results()
        match.player2.initialize_results()

    for match in matches:
        if match.round.tournament_stage > 0:
            continue

        match.player1.matched.add(match.player2)
        match.player2.matched.add(match.player1)

        if match.score1 > match.score2:
            match.player1.increase_wins(match.player2)
            match.player2.increase_loses(match.player1)
            if match.score1 == 1:
                match.player1.increase_half_wins()
                match.player2.increase_half_loses()
        elif match.score2 > match.score1:
            match.player2.increase_wins(match.player1)
            match.player1.increase_loses(match.player2)
            if match.score2 == 1:
                match.player2.increase_half_wins()
                match.player1.increase_half_loses()
        else:
            match.player2.increase_draws()
            match.player1.increase_draws()

        if m_league.win_mode == 'half':
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
        else:
            if match.score1 > match.score2:
                match.player1.increase_score(2)
            elif match.score2 > match.score1:
                match.player2.increase_score(2)
            else:
                match.player1.increase_score(1)
                match.player2.increase_score(1)


def calculate_rankings(league: League, players: List[Player], matches: List[Match]) -> None:
    for m_player in players:
        m_player.initialize_ranking()
        m_player.buchholz = sum([opponent.score for opponent in m_player.matched])

    # dict_players_by_first
    dict_players_by_first = {}
    for m_player in players:
        first_value = m_player.get_ranking_first(league)
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
                if m_match.round.tournament_stage > 0:
                    continue

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
                            key=lambda p: p.get_ranking_first(league) + (p.all_kill,) + p.get_ranking_second(league),
                            reverse=True)
    for idx, m_player in enumerate(sorted_players):
        m_player.ranking = idx+1


def get_players_order_by_ranking(m_league: League) -> List[Player]:
    players, matches = m_league.get_players_and_matches()  # type: List[Player], List[Match]
    calculate_matches_result(m_league, matches)
    calculate_rankings(m_league, players, matches)

    players = sorted(players, key=lambda p: p.ranking)  # type: List[Player]

    return [m_player for m_player in players if m_player.is_ghost is False]
