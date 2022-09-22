import random
from typing import Set, Optional, List

from swiss.core import lib_league
from swiss.models.league import League
from swiss.models.player import Player
from swiss.models.round import Round
from swiss.models.match import Match


def start_new_round(m_league: League) -> Optional[Round]:
    rounds = m_league.rounds.all()

    new_matches = _get_matches_of_new_round(m_league)
    if new_matches is None:
        return None

    m_round = Round.objects.create(league=m_league, no=len(rounds) + 1)

    for player1, player2 in new_matches:
        Match.objects.create(league=m_league, round=m_round, player1=player1, player2=player2,
                             score1=(2 if m_league.win_mode == 'half' else 1) if player2.is_ghost is True else 0)

    return m_round


def _get_matches_of_new_round(m_league: League) -> Optional[list]:
    result = []

    # matches 플레이어 초기화
    players, matches = m_league.get_players_and_matches()     # type: List[Player], List[Match]
    lib_league.calculate_matches_result(m_league, matches)

    # 부전승은 항상 제일 마지막에 나오도록 하기 위함
    for m_player in players:
        if m_player.is_ghost:
            m_player.wins = -1
            m_player.score = -1

    _calculate_family(players)

    # 드랍한 사용자 제외
    candidates = {player for player in players if player.is_dropped is False}
    # 플레이어가 홀수라면 고스트 제외
    if len(candidates) % 2 != 0:
        candidates = {player for player in candidates if player.is_ghost is False}

    # reserved_player1 팝 되었을 때 대상 플레이어1을 저장
    reserved_player1 = None
    # blacklist 플레이어2 후보에서 제외할 플레이어
    blacklist = set()
    # result_stack 최종 결과를 저장하기 위한 스택
    result_stack = []
    while len(candidates) > 0:
        if reserved_player1:
            player1 = reserved_player1
            reserved_player1 = None
        else:
            player1 = _choose_first_player(candidates)
            candidates.remove(player1)

        player2 = _choose_second_player(player1, candidates - blacklist)

        if player2:
            candidates.remove(player2)
            result_stack.append((player1, player2, blacklist))
            blacklist = set()
        # 상대를 찾지 못한 경우
        else:
            # 첫 매치의 경우라면 라운드를 만들 수 없는 상태
            if len(result_stack) <= 0:
                return None

            reserved_player1, popped_player2, blacklist = result_stack.pop()

            candidates.add(player1)
            candidates.add(popped_player2)
            blacklist.add(popped_player2)

    for player1, player2, blacklist in result_stack:
        result.append((player1, player2))

    # 부전승이 들어간 경기는 제일 마지막에 넣는다
    for idx, value in enumerate(result):
        player1, player2 = value
        if player2.is_ghost:
            match = result.pop(idx)
            result.append(match)
            break

    return result


def _calculate_family(players: List[Player]) -> None:
    for m_player in players:
        if not m_player.is_family:
            continue
        family_member_ids = m_player.family.values_list('id', flat=True)
        family = {p for p in players if (p.id in family_member_ids)}
        m_player.matched.update(family)


def _choose_first_player(players: Set[Player]) -> Optional[Player]:
    if len(players) <= 0:
        return None

    _calculate_matched_others(players)

    sorted_players = sorted(players,
                            # key=lambda p: (p.wins, len(p.matched_same), len(p.matched_lower), random.random()),
                            key=lambda p: (p.score, random.random()),
                            reverse=True)
    return sorted_players[0]


def _choose_second_player(player: Player, players: Set[Player]) -> Optional[Player]:
    if len(players) <= 0:
        return None

    candidates = set(players)

    # 이번 상대는 제외
    if player in candidates:
        candidates.remove(player)

    # 이미 대전한 상대는 제외
    for matched_player in player.matched:
        if matched_player in candidates:
            candidates.remove(matched_player)

    # 대전할 상대가 없는 경우
    if len(candidates) <= 0:
        return None

    _calculate_matched_others(candidates)

    sorted_players = sorted(candidates,
                            # key=lambda p: (p.wins, len(p.matched_same), len(p.matched_lower), random.random()),
                            key=lambda p: (p.score, random.random()),
                            reverse=True)
    return sorted_players[0]


def _calculate_matched_others(players: Set[Player]) -> None:
    # players_by_score 점수별 플레이어 목록
    players_by_score = {}
    for player in players:
        if player.score not in players_by_score:
            players_by_score[player.score] = set()
        players_by_score[player.score].add(player)

    for (score, players) in players_by_score.items():
        # players_lower 바로 밑의 승수 플레이어 목록
        players_lower = set()
        for lower_score in range(score-1, -1, -1):
            if lower_score in players_by_score:
                players_lower = players_by_score[lower_score]
                break

        # matched_same & matched_lower 계산
        for player in players:
            player.matched_same = player.matched & players
            player.matched_lower = player.matched & players_lower
