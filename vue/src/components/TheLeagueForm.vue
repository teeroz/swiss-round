<template>
  <div class="container my-4">
    <form class="container" @submit.prevent="submit">
      <div class="row form-group">
        <label for="exampleInputTitle">제목</label>
        <input ref="title" type="text" class="form-control" aria-describeBy="TitleHelp" :placeholder="defaultTitle" maxlength="32" v-model="league.title" autofocus />
        <small id="TitleHelp" class="form-text text-muted">입력하지 않을 경우 오늘 날짜로 입력됩니다.</small>
      </div>
      <div class="row form-check mb-3">
        <input id="WinMode" type="checkbox" class="form-check-input" value="half" v-model="league.win_mode" :disabled="editMode" />
        <label class="form-check-label" for="WinMode">판정승 모드</label>
        <small id="WinModeHelp" class="form-text text-muted">승패를 입력할 때 ½승,½패 상태도 입력할 수 있습니다.</small>
      </div>
      <div class="row form-check mb-3">
        <input id="RankingCriteria" type="checkbox" class="form-check-input" value="winner" v-model="league.ranking_criteria" />
        <label class="form-check-label" for="RankingCriteria">승자승원칙 우선</label>
        <small id="RankingCriteriaHelp" class="form-text text-muted">승자승원칙, 부크홀츠 순으로 순위를 결정합니다.</small>
      </div>
      <div class="row form-group">
        <label for="exampleInputTie">순위</label>
        <select class="form-control mb-1" disabled>
          <option>{{ league.win_mode ? '점수' : '승수' }}</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>{{ league.ranking_criteria ? '승자승원칙' : '부크홀츠' }}</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>{{ league.ranking_criteria ? '부크홀츠' : '승자승원칙' }}</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>최대연승수</option>
        </select>
        <select class="form-control my-1" disabled>
          <option>연승시작라운드</option>
        </select>
        <small id="descriptionHelp" class="form-text text-muted">위 순서에 따라 순위가 결정됩니다.</small>
      </div>
      <div class="row justify-content-end">
        <button type="button" class="btn btn-secondary col-2 mx-2" @click="cancel">취소</button>
        <button type="submit" class="btn btn-primary col-2">확인</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'TheLeagueForm',

  props: {
    league: {
      type: Object,
      required: true
    },
    defaultTitle: {
      type: String,
      required: true
    },
    editMode: {
      type: Boolean,
      required: false
    },
    submitCallback: {
      type: Function,
      required: true
    }
  },

  mounted: function () {
    this.$refs.title.focus()
  },

  methods: {
    cancel: function () {
      this.$router.go(-1)
    },

    submit: function () {
      if (this.league.title) {
        this.league.title = this.league.title.trim()
      }

      if (!this.league.title || this.league.title.length <= 0) {
        this.league.title = this.defaultTitle
      }

      this.league.win_mode = this.league.win_mode ? 'half' : ''
      this.league.ranking_criteria = this.league.ranking_criteria ? 'winner' : ''

      this.submitCallback()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

