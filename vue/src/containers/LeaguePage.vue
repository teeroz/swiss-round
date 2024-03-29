<template>
  <div>
    <the-navbar :title="league.title" :goBack="goBack">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="print">프린트</button>
          <div class="dropdown-divider"></div>
          <button type="button" class="dropdown-item" @click="edit">수정</button>
          <div class="dropdown-divider"></div>
          <button type="button" class="dropdown-item" @click="remove">삭제</button>
        </div>
      </div>
    </the-navbar>

    <the-loading ref="loading">
      <ul class="nav nav-tabs mt-2 league-tab">
        <li class="nav-item">
          <span class="nav-link" :class="{active: mode === 'PLAYERS'}" @click="showPlayers">
            플레이어
            <span 
                class="badge badge-pill" 
                :class="{'badge-primary': mode === 'PLAYERS', 'badge-secondary': mode !== 'PLAYERS'}"
                >
              {{ players.length }}
            </span>
          </span>
        </li>
        <li class="nav-item" @click="showRounds">
          <span class="nav-link" :class="{active: mode === 'ROUNDS'}">
            라운드
            <span 
                class="badge badge-pill" 
                :class="{'badge-primary': mode === 'ROUNDS', 'badge-secondary': mode !== 'ROUNDS'}"
                >
              {{ rounds.length }}
            </span>
          </span>
        </li>
        <li class="nav-item" @click="showTournaments">
          <span class="nav-link" :class="{active: mode === 'TOURNAMENTS'}">
            토너먼트
            <span
                class="badge badge-pill"
                :class="{'badge-primary': mode === 'TOURNAMENTS', 'badge-secondary': mode !== 'TOURNAMENTS'}"
                >
              {{ tournaments.length }}
            </span>
          </span>
        </li>
      </ul>

      <div class="list-group" v-if="mode === 'PLAYERS'">
        <router-link
           v-for="player in players"
           :to="{name: 'player', params: {league_id: player.league, player_id: player.id}}"
           :key="player.id"
           class="list-group-item list-group-item-action border-left-0 border-right-0"
           >
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <span class="badge badge-secondary badge-pill">{{ player.ranking }}</span>
              <span :class="{'dropped': player.is_dropped, 'text-muted': player.is_dropped}">
                {{ player.name }}
              </span>
            </div>
            <small class="text-muted" v-if="player.wins + player.draws + player.loses > 0">
              <template v-if="league.win_mode === 'half'">
                승 {{ player.wins - player.half_wins }}-{{ player.half_wins }}-{{ player.draws }}-{{player.half_loses}}-{{ player.loses - player.half_loses }} 패
              </template>
              <template v-else>
                <template v-if="player.wins > 0">{{ player.wins }}승 </template>
                <template v-if="player.draws > 0">{{ player.draws }}무 </template>
                <template v-if="player.loses > 0">{{ player.loses }}패</template>
              </template>
              <template><span style="color: #CFCFCF;"> | </span> {{ player.score }}점</template>
              <template v-if="league.ranking_criteria === 'winner'">
                <template v-if="player.all_kill > 0"> / 승자승</template>
                <span style="color: #CFCFCF;"> | </span> {{ player.buchholz }} bh
              </template>
              <template v-else>
                <span style="color: #CFCFCF;"> | </span> {{ player.buchholz }} bh
                <template v-if="player.all_kill > 0"> <span style="color: #CFCFCF;"> | </span> 승자승</template>
              </template>
              <span style="color: #CFCFCF;"> | </span> {{ player.max_strikes_count }}연승
            </small>
          </div>
        </router-link>

        <router-link
           :to="{name: 'playerAdd', params: {league_id: league.id}}"
           class="list-group-item list-group-item-action border-left-0 border-right-0 text-center text-primary"
           :class="{'mt-1': players.length <= 0}"
           >
          <i class="fas fa-user-plus"></i> <strong><span> 플레이어 추가하기</span></strong>
        </router-link>
      </div>

      <div class="list-group" v-if="mode === 'ROUNDS'">
        <router-link
           v-for="round in rounds"
           :to="{name: 'round', params: {league_id: round.league, round_id: round.id}}"
           :key="round.id"
           class="list-group-item list-group-item-action border-left-0 border-right-0"
           >
          {{ round.no }} 라운드
        </router-link>

        <span
           class="list-group-item list-group-item-action border-left-0 border-right-0 text-center text-primary"
           :class="{'mt-1': rounds.length <= 0}"
           @click="startNewRound"
           >
          <i class="fas fa-trophy"></i> <strong><span> 새 라운드 시작하기</span></strong>
        </span>
      </div>

      <div class="list-group" v-if="mode === 'TOURNAMENTS'">
        <router-link
           v-for="tournament in tournaments"
           :to="{name: 'tournament', params: {league_id: tournament.league, round_id: tournament.id}}"
           :key="tournament.id"
           class="list-group-item list-group-item-action border-left-0 border-right-0"
           >
          {{ tournament.tournament_stage === 2 ? '결승' : tournament.tournament_stage + '강' }}
        </router-link>

        <router-link
           v-if="tournaments.length <= 0"
           :to="{name: 'tournamentCreate', params: {league_id: league.id, player_num: players.length}}"
           class="list-group-item list-group-item-action border-left-0 border-right-0 text-center text-primary"
           :class="{'mt-1': tournaments.length <= 0}"
           >
          <i class="fas fa-user-plus"></i> <strong><span> 새 토너먼트 시작하기</span></strong>
        </router-link>
      </div>
    </the-loading>

    <div style="display: none;">
      <div id="printArea">
        <div class="row justify-content-center" style="margin: 30px;">
          <h1 class="col-12 text-center display-4" style="margin-bottom: 30px;">플레이어 순위</h1>

          <table class="table table-bordered col-12 text-center" style="font-size: 24px;">
            <thead>
                <th scope="col">순위</th>
                <th scope="col">Player</th>
                <th scope="col">승패</th>
                <th scope="col">점수</th>
                <th scope="col">부크홀츠</th>
                <th scope="col">최대연승</th>
                <th scope="col">기타</th>
            </thead>
            <tbody>
              <template v-for="player in players">
                <tr :key="player.id">
                  <td>{{ player.ranking }} 위</td>
                  <td>{{ player.name }}</td>
                  <td>
                    <template v-if="league.win_mode === 'half'">
                      승 {{ player.wins - player.half_wins }}-{{ player.half_wins }}-{{ player.draws }}-{{player.half_loses}}-{{ player.loses - player.half_loses }} 패
                    </template>
                    <template v-else>
                      <template v-if="player.wins > 0">{{ player.wins }}승 </template>
                      <template v-if="player.draws > 0">{{ player.draws }}무 </template>
                      <template v-if="player.loses > 0">{{ player.loses }}패</template>
                    </template>
                  </td>
                  <td>{{ player.score }} 점</td>
                  <td>{{ player.buchholz }} 점</td>
                  <td>{{ player.max_strikes_count }} 연승</td>
                  <td><template v-if="player.all_kill > 0">승자승</template></td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeaguePage',

  data: function () {
    let mode = 'PLAYERS'
    if (this.$route.query.mode) {
      mode = this.$route.query.mode
    }

    return {
      league: { id: 0, title: '' },
      players: [],
      rounds: [],
      tournaments: [],
      mode: mode
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}`)
      .then(res => {
        this.league = res.data.league
        this.players = res.data.players
        this.rounds = res.data.rounds
        this.tournaments = res.data.tournaments
        this.$refs.loading.stop()
      })
  },

  methods: {
    goBack: function () {
      this.$router.push({ name: 'leagues' })
    },

    print: function () {
      this.$htmlToPaper('printArea');
    },

    edit: function () {
      this.$router.push({ name: 'leagueEdit', params: { league_id: this.$route.params.league_id } })
    },

    remove: function () {
      if (!confirm('정말로 이 리그를 삭제하시겠습니까?')) {
        return
      }

      this.$refs.loading.start()
      this.$axios.swiss.delete(`league/${this.$route.params.league_id}`)
        .then(this.goBack)
    },

    showPlayers: function () {
      this.$router.replace({ name: 'league', params: { league_id: this.$route.params.league_id }, query: { mode: 'PLAYERS' } })
      this.mode = 'PLAYERS'
    },

    showRounds: function () {
      this.$router.replace({ name: 'league', params: { league_id: this.$route.params.league_id }, query: { mode: 'ROUNDS' } })
      this.mode = 'ROUNDS'
    },

    showTournaments: function () {
      this.$router.replace({ name: 'league', params: { league_id: this.$route.params.league_id }, query: { mode: 'TOURNAMENTS' } })
      this.mode = 'TOURNAMENTS'
    },

    startNewRound: function () {
      if (this.players.length <= 1) {
        alert('참가할 수 있는 플레이어가 없습니다.')
        return
      }

      this.$refs.loading.start()

      this.$axios.swiss.post(`league/${this.$route.params.league_id}/round`)
        .then(res => {
          if (!res.data['id']) {
            alert('더 이상 라운드를 만들 수 없습니다.')
            this.$refs.loading.stop()
            return
          }

          this.$router.push({ name: 'round', params: { league_id: this.league.id, round_id: res.data.id } })
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .dropped {
    text-decoration: line-through;
  }
</style>
