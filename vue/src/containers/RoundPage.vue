<template>
  <div>
    <the-navbar :title="round.no + ' 라운드'" :goBack="goBack">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="printRound">라운드별 프린트</button>
          <div class="dropdown-divider"></div>
          <button type="button" class="dropdown-item" @click="remove">삭제</button>
        </div>
      </div>
    </the-navbar>

    <the-loading ref="loading">
      <div class="list-group">
        <span
           v-for="(match, index) in matches"
           :key="match.id"
           class="list-group-item border-left-0 border-right-0"
           >
          <div class="d-flex justify-content-center">
            <div class="col-6 text-right">
              <span @click="goPlayerPage(match.player1)">
                <template><small>{{ match.player1.score }}점</small> {{ match.player1.name }} </template>
              </span>

              <template v-if="league.win_mode === 'half'">
                <button 
                  type="button" 
                  class="btn btn-sm ml-1"
                  :class="{'btn-secondary': match.score1 === match.score2, 'btn-primary': match.score1 === 2, 'btn-outline-primary': match.score1 === 1, 'btn-danger': match.score2 === 2, 'btn-outline-danger': match.score2 === 1}"
                  @click="updateScore(match, match.score2 === 0 ? Math.min(match.score1 + 1, 2) : 0, match.score2 === 0 ? 0 : match.score2 - 1)"
                  >
                  <template v-if="match.score1 > match.score2">{{ match.score1 === 1 ? '½' : '' }}승</template>
                  <template v-else-if="match.score1 < match.score2">{{ match.score2 === 1 ? '½' : '' }}패</template>
                  <template v-else>무</template>
                </button>
              </template>
              <template v-else>
                <button 
                  type="button" 
                  class="btn btn-sm ml-1"
                  :class="{'btn-secondary': match.score1 === match.score2, 'btn-primary': match.score1 > match.score2, 'btn-danger': match.score1 < match.score2}"
                  @click="updateScore(match, match.score1 ? 0 : 1, 0)"
                  >
                  <template v-if="match.score1 > match.score2">승</template>
                  <template v-else-if="match.score1 < match.score2">패</template>
                  <template v-else>무</template>
                </button>
              </template>
            </div>
            <div><small>#{{ index + 1 }}</small></div>
            <div class="col-6 text-left">
              <template v-if="league.win_mode === 'half'">
                <button 
                  type="button" 
                  class="btn btn-sm ml-1"
                  :class="{'btn-secondary': match.score1 === match.score2, 'btn-primary': match.score2 === 2, 'btn-outline-primary': match.score2 === 1, 'btn-danger': match.score1 === 2, 'btn-outline-danger': match.score1 === 1}"
                  @click="updateScore(match, match.score1 === 0 ? 0 : match.score1 - 1, match.score1 === 0 ? Math.min(match.score2 + 1, 2) : 0)"
                  >
                  <template v-if="match.score2 > match.score1">{{ match.score2 === 1 ? '½' : '' }}승</template>
                  <template v-else-if="match.score2 < match.score1">{{ match.score1 === 1 ? '½' : '' }}패</template>
                  <template v-else>무</template>
                </button>
              </template>
              <template v-else>
                <button 
                  type="button" 
                  class="btn btn-sm mr-1"
                  :class="{'btn-secondary': match.score2 === match.score1, 'btn-primary': match.score2 > match.score1, 'btn-danger': match.score2 < match.score1}"
                  @click="updateScore(match, 0, match.score2 ? 0 : 1)"
                  >
                  <template v-if="match.score2 > match.score1">승</template>
                  <template v-else-if="match.score2 < match.score1">패</template>
                  <template v-else>무</template>
                </button>
              </template>

              <span @click="goPlayerPage(match.player2)">
                <template> {{ match.player2.name }} <small>{{ match.player2.score }}점</small></template>
              </span>
            </div>
          </div>
        </span>
      </div>

      <div class="text-center my-3">
        <button 
          type="button" 
          class="btn" 
          :class="{'btn-primary': isComplete, 'btn-secondary': !isComplete}"
          @click="nextRound"
          :disabled="!isComplete">
          <i class="fas fa-arrow-right"></i> <strong><span> 다음 라운드 시작하기</span></strong>
        </button>
      </div>
    </the-loading>

    <div style="display: none;">
      <div id="printAreaGroupByTable">
        <div class="row justify-content-center" style="margin: 30px;">
          <h1 class="col-12 text-center display-4" style="margin-bottom: 30px;">{{ round.no }} 라운드</h1>

          <table class="table table-bordered col-12 text-center" style="font-size: 24px;">
            <thead>
                <th scope="col">#</th>
                <th scope="col">Player 1</th>
                <th scope="col">Player 2</th>
                <th scope="col">#</th>
                <th scope="col">Player 1</th>
                <th scope="col">Player 2</th>
            </thead>
            <tbody>
              <template v-for="matches in matchesByTable">
                <tr :key="matches[0].id">
                  <template v-for="match in matches">
                    <td :key="match.id + '_1'">{{ match.no }}</td>
                    <td :key="match.id + '_2'">{{ match.player1.name }}</td>
                    <td :key="match.id + '_3'">{{ match.player2.name }}</td>
                  </template>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>

      <div id="printAreaGroupByPlayer">
        PRINT BY PLAYER
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  name: 'RoundPage',

  data: function () {
    return {
      league: { win_mode: '' },
      round: { no: '' },
      matches: [],
      matchesByTable: [],
      isComplete: false
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}/round/${this.$route.params.round_id}`)
      .then(res => {
        // matches 에 no 추가 
        const matches = res.data.matches;
        let no = 1;
        // eslint-disable-next-line
        for (const match of matches) {
          match.no = no;
          no += 1;
        }

        this.league = res.data.league
        this.round = res.data.round
        this.matches = res.data.matches
        this.checkIsComplete()
        this.$refs.loading.stop()

        // 테이블별로 2개씩 청크로 만들어서 저장한다
        const matches1 = matches.slice(0, Math.floor((matches.length + 1) / 2));
        const matches2 = matches.slice(Math.floor((matches.length + 1) / 2));
        const matchesByTable = [];
        // eslint-disable-next-line
        for (const k in matches1) {
          matchesByTable.push(matches1[k]);
          if (matches2.length > k) {
            matchesByTable.push(matches2[k]);
          }
        }
        this.matchesByTable = _.chunk(matchesByTable, 2);
      })
  },

  methods: {
    goBack: function () {
      this.$router.push({ name: 'league', params: { id: this.$route.params.league_id }, query: { mode: 'ROUNDS' } })
    },

    printRound: function () {
      this.$htmlToPaper('printAreaGroupByTable');
    },

    printPlayer: function () {
    },

    remove: function () {
      if (!confirm('정말로 이 라운드를 삭제하시겠습니까?')) {
        return false
      }

      this.$refs.loading.start()
      this.$axios.swiss.delete(`league/${this.$route.params.league_id}/round/${this.$route.params.round_id}`)
        .then(this.goBack)
    },

    nextRound: function () {
      this.$refs.loading.start()

      this.$axios.swiss.post(`league/${this.$route.params.league_id}/round`)
        .then(res => {
          if (!res.data['id']) {
            alert('더 이상 라운드를 만들 수 없습니다.')
            this.$refs.loading.stop()
            return
          }

          this.$router.push({ name: 'round', params: { league_id: this.$route.params.league_id, round_id: res.data.id } })
        })
    },

    updateScore: function (match, score1, score2) {
      match.score1 = score1
      match.score2 = score2

      this.$axios.swiss.put(`league/${this.$route.params.league_id}/round/${this.$route.params.round_id}/match/${match.id}`,
        {score1: score1, score2: score2})
        .then(res => {
          this.matches = res.data.matches
          this.checkIsComplete()
        })
    },

    goPlayerPage: function (player) {
      if (player.is_ghost) {
        return
      }

      this.$router.push({ name: 'player', params: { league_id: this.$route.params.league_id, player_id: player.id } })
    },

    checkIsComplete: function () {
      let isComplete = true
      // eslint-disable-next-line
      for (const key in this.matches) {
        const match = this.matches[key]
        if (match.score1 === match.score2) {
          isComplete = false
          break
        }
      }
      this.isComplete = isComplete
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
