<template>
  <div>
    <the-navbar :title="player.name">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="editBasic">수정</button>
          <div class="dropdown-divider"></div>
          <template v-if="player.is_dropped">
            <button type="button" class="dropdown-item" @click="undrop">참가</button>
          </template>
          <template v-else>
            <button type="button" class="dropdown-item" @click="drop">드랍</button>
          </template>
          <div class="dropdown-divider"></div>
          <button type="button" class="dropdown-item" @click="editFamily">가족설정</button>
        </div>
      </div>
    </the-navbar>

    <the-loading ref="loading">
      <div class="container">
        <div class="card my-4">
          <div class="card-header text-white bg-secondary">
            기본정보
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>이름</span>
              <span class="text-muted">{{ player.name }}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center" v-if="player.memo">
              <span>메모</span>
              <span class="text-muted">{{ player.memo }}</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center" v-if="player.family.length > 0">
              <span>가족</span>
              <span class="text-muted">
                <template v-for="(familyMember, index) in player.family">
                  {{ familyMember.name }}<template v-if="index+1 < player.family.length">,</template>
                </template>
              </span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>상태</span>
              <span class="text-muted">{{ player.is_dropped ? '기권' : '참가중' }}</span>
            </li>
          </ul>
        </div>

        <div class="card my-4">
          <div class="card-header text-white bg-secondary">
            성적
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>순위</span>
              <span class="text-muted">{{ player.ranking }}위</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>승패</span>
              <span class="text-muted">
                <template v-if="league.win_mode === 'half'">
                  승 {{ player.wins - player.half_wins }}-{{ player.half_wins }}-{{ player.draws }}-{{player.half_loses}}-{{ player.loses - player.half_loses }} 패
                </template>
                <template v-else>
                  <template v-if="player.wins > 0">{{ player.wins }}승 </template>
                  <template v-if="player.draws > 0">{{ player.draws }}무 </template>
                  <template v-if="player.loses > 0">{{ player.loses }}패</template>
                </template>
              </span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>점수</span>
              <span class="text-muted">{{ player.score }}점</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>부크홀츠</span>
              <span class="text-muted">{{ player.buchholz }} bh</span>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>최대연승</span>
              <span class="text-muted">
                <template v-if="player.max_strikes_count > 0">
                  {{ player.max_strikes_count }}연승
                </template>
                <template v-if="player.max_strikes_count <= 0">
                  X
                </template>
              </span>
            </li>
          </ul>
        </div>

        <div class="card my-4" v-if="matches.length > 0">
          <div class="card-header text-white bg-secondary">
            대전기록
          </div>
          <ul class="list-group list-group-flush">
            <li 
              v-for="match in matches"
              :key="match.id"
              class="list-group-item d-flex justify-content-between align-items-center" 
              >
              <span @click="goPlayerPage(match.opponent)">
                <small>vs</small> {{ match.opponent.name }} 
                <small class="text-muted">
                  <template>{{ match.opponent.score }}점</template>
                </small>
              </span>

              <button v-if="league.win_mode === 'half'"
                type="button"
                class="btn btn-sm ml-1"
                :class="{'btn-secondary': match.result === 'D',
                         'btn-primary': match.result === 'W' && !match.half_win,
                         'btn-outline-primary': match.result === 'W' && match.half_win,
                         'btn-danger': match.result === 'L' && !match.half_win,
                         'btn-outline-danger': match.result === 'L' && match.half_win}"
                >
                <template v-if="match.result === 'W'">{{ match.half_win ? '½' : '' }}승</template>
                <template v-else-if="match.result === 'L'">{{ match.half_win ? '½' : '' }}패</template>
                <template v-else>무</template>
              </button>
              <button v-else
                type="button" 
                class="btn btn-sm ml-1"
                :class="{'btn-secondary': match.result === 'D',
                         'btn-primary': match.result === 'W',
                         'btn-danger': match.result === 'L'}"
                >
                <template v-if="match.result === 'W'">승</template>
                <template v-else-if="match.result === 'L'">패</template>
                <template v-else>무</template>
              </button>
            </li>
          </ul>
        </div>
      </div>
    </the-loading>
  </div>
</template>

<script>
export default {
  name: 'PlayerPage',

  data: function () {
    return {
      league: { win_mode: '' },
      player: { id: 0, name: '', family: [] },
      matches: []
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`)
      .then(res => {
        this.league = res.data.league
        this.player = res.data.player
        this.matches = res.data.matches
        this.$refs.loading.stop()
      })
  },

  methods: {
    editBasic: function () {
      this.$router.push({ name: 'playerEditBasic', params: { league_id: this.$route.params.league_id, player_id: this.$route.params.player_id } })
    },

    editFamily: function () {
      this.$router.push({ name: 'playerEditFamily', params: { league_id: this.$route.params.league_id, player_id: this.$route.params.player_id } })
    },

    drop: function () {
      this.$refs.loading.start()
      this.$axios.swiss.put(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`, { is_dropped: true })
        .then(res => {
          this.player = res.data.player
          this.$refs.loading.stop()
        })
    },

    undrop: function () {
      this.$refs.loading.start()
      this.$axios.swiss.put(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`, { is_dropped: false })
        .then(res => {
          this.player = res.data.player
          this.$refs.loading.stop()
        })
    },

    goPlayerPage: function (player) {
      if (player.is_ghost) {
        return
      }

      this.$router.push({ name: 'player', params: { league_id: this.$route.params.league_id, player_id: player.id } })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
