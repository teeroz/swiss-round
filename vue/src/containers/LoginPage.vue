<template>
  <div>
    <the-navbar mode="HOME">
      <div>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="logout">로그아웃</button>
        </div>
      </div>
    </the-navbar>

    <div class="container">
      <div class="card mt-3">
        <div class="card-body">
          <div class="text-center mb-5">
            <!--
            <div class="row justify-content-center mb-2">
              <img src="/static/facebook-login.png" width="222" height="49" @click="authenticate('facebook')" />
            </div>
            -->
            <div class="row justify-content-center mb-2">
              <img src="/static/kakao-login.png" width="222" height="49" @click="authenticate('github')" />
            </div>
            <div class="row justify-content-center mb-2">
              <input ref="username" type="text" class="form-control mr-1" style="width: 150px;" placeholder="username" maxlength="20">
              <button type="button" class="btn btn-primary" @click="login()">로그인</button>
            </div>
          </div>

          <h5 class="card-title">공지</h5>
          <p class="card-text mb-4">
            <small>
              - 예상보다 사용량이 많아서 3개월이 지난 리그 데이타는 삭제할 예정입니다. 이점 양해 부탁드립니다.
            </small>
          </p>

          <h5 class="card-title">변경사항</h5>
          <p class="card-text mb-4">
            <small>
              <strong>v1.7.0</strong>&nbsp;&nbsp;<span class="text-muted">at 2023.05.08</span><br />
              - 토너먼트 기능을 추가하였습니다. 스위스 리그를 완료한 후, 토너먼트를 만들면 리그 순위에 기반하여 토너먼트 대진표를 작성해줍니다.<br />
            </small>
            <small>
              <strong>v1.6.0</strong>&nbsp;&nbsp;<span class="text-muted">at 2022.09.27</span><br />
              - 순위 계산을 모두 점수제로 변경합니다. 일반적으로 승 2점 / 무 1점 / 패 0점으로 처리합니다.<br />
            </small>
            <small>
              <strong>v1.5.0</strong>&nbsp;&nbsp;<span class="text-muted">at 2022.09.22</span><br />
              - 장기의 점수승을 지원하기 위하여 판정승(1/2승) 기능을 추가하였습니다. 이 모드에서는 완승 7점 / 점수승 4점 / 점수패 2점 / 완패 0점의 점수를 부여하며,
              순위 결정할 때 점수를 최우선순위로 합니다.<br />
              - 순위 결정할 때 승자승원칙을 우선으로 할 수 있도록 승자승원칙 우선 기능을 추가하였습니다.
              이 모드에서는 순위를 결정할 때 부크홀츠보다 승자승을 더 우선으로 합니다.<br />
            </small>
            <small>
              <strong>v1.4.0</strong>&nbsp;&nbsp;<span class="text-muted">at 2019.05.18</span><br />
              - 일반 아이디로 로그인하는 기능을 추가하였습니다. 이 기능을 이용하면 여러명이 로그인하여 함께 사용할 수 있습니다. 단, 비밀번호는 없으니 주의해주세요.<br />
              - 플레이어 순위 프린트 기능과 라운드 표 프린트 기능이 추가되었습니다. 각 화면에서 우측 상단의 메뉴를 열어보세요.<br />
            </small>
            <small>
              <strong>v1.3.0</strong>&nbsp;&nbsp;<span class="text-muted">at 2018.05.28</span><br />
              - 카카오 계정으로 로그인 하기 추가<br />
            </small>
            <small>
              <strong>v1.2.2</strong>&nbsp;&nbsp;<span class="text-muted">at 2018.01.11</span><br />
              - 승점 계산할 때 승 3점, 무 1점으로 변경 (기존 승 2점, 무 1점) <br />
              - 리그 생성할 때 로그인 화면으로 튕기는 버그 픽스 <br />
              - 리그 플레이어 목록에서 경기 시작 전에 승무패 표시하지 않도록 수정 <br />
            </small>
          </p>

          <h5 class="card-title">소개</h5>
          <p class="card-text mb-1">
            <small>
              스위스 라운드 방식의 리그를 위한 비영리 목적의 어플입니다. 
              사설 리그를 운영하기 위하여 만들었으나 필요한 분들을 위하여 공개하였습니다.
              사용하면서 궁금한 점이나 개선에 대한 의견이 있으면 이메일로 연락주세요. <br />
              후원 계좌 : 카카오뱅크 7979-7979-328 신종훈 <br />
              <span class="text-muted">by prophet75 at gmail.com</span>
            </small>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',

  data: function () {
    return { }
  },

  methods: {
    authenticate: function (provider) {
      this.$auth.authenticate(provider)
        .then(res => {
          this.$auth.user = {
            id: res.data.id,
            name: res.data.name
          }
          this.$router.push({ name: 'leagues' })
        })
    },

    login: function () {
      if (!this.$refs.username.value) {
        alert('로그인 아이디를 입력해주세요.')
        return
      }

      this.$auth.login({ username: this.$refs.username.value }).then(res => {
        this.$auth.user = {
          id: res.data.name,
          name: res.data.name
        }
        this.$router.push({ name: 'leagues' })
      })
    },
    
    logout: function () {
      this.$auth.logout()
      this.$router.push({ name: 'login' })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
