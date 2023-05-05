<template>
  <div>
    <the-navbar title="토너먼트 만들기">
    </the-navbar>

    <div class="container form-group">
      <div class="card mt-3">
        <ul class="list-group list-group-flush">
          <li
            v-for="stage in stages"
            :key="stage"
            class="list-group-item align-items-center"
            >
            <div class="form-check ml-4 mb-0">
              <input
                type="radio"
                class="form-check-input"
                style="margin-top: .4rem!important"
                :id="'checkbox_' + stage"
                :value="stage"
                v-model="selectedStage"
                >
              <label class="form-check-label pl-1" :for="'checkbox_' + stage">{{ stage + '강' }}</label>
            </div>
          </li>
        </ul>
      </div>

      <div class="d-flex justify-content-end mt-3">
        <button type="button" class="btn btn-secondary col-2 mx-2" @click="cancel">취소</button>
        <button type="submit" class="btn btn-primary col-2" @click="submit">확인</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TournamentCreatePage',

  data: function () {
    const stages = []
    for (let i=4; i<this.$route.params.player_num; i*=2) {
      stages.push(i)
    }

    return {
      stages,
      selectedStage: 0
    }
  },

  methods: {
    cancel: function () {
      this.$router.go(-1)
    },

    submit: function () {
      this.$axios.swiss.post(`league/${this.$route.params.league_id}/tournament`,
                            { 'stage': this.selectedStage })
        .then(() => this.$router.go(-1))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
