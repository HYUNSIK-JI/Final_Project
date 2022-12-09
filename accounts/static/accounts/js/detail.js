//프로필 카테고리
$(document).ready(function () {
  // 탭을 클릭하면
  $('ul.tabs li').click(function () {
    // 그 탭의 data-tab을 들고옴
    var tab_id = $(this).attr('data-tab');
    // 모든 탭의 li와 div를 제거함
    $('ul.tabs li').removeClass('current');
    $('.tab-content').removeClass('current');
    //클릭한 탭의 클래스, id에 current를 더함
    $(this).addClass('current');
    $("#" + tab_id).addClass('current');
  })

})
document.querySelector('.down2').addEventListener('click', function (e) {
  const option_value = e.target.value
  const articlescomment = document.querySelector('#my-to-notes')
  const freescomment = document.querySelector('#my-from-notes')
  // 전체
  if (option_value == 6) {
    articlescomment.setAttribute('class', 'option-active')
    freescomment.setAttribute('class', 'option-active')
  }
  // 질문
  else if (option_value == 7) {
    articlescomment.setAttribute('class', 'option-active')
    freescomment.setAttribute('class', 'option-inactive')
  }
  // 자유
  else {
    articlescomment.setAttribute('class', 'option-inactive')
    freescomment.setAttribute('class', 'option-active')
  }
})

document.querySelector('.down').addEventListener('click', function (e) {
  const option_value = e.target.value
  const articles = document.querySelector('#my-articles')
  const frees = document.querySelector('#my-frees')
  // 전체
  if (option_value == 0) {
    articles.setAttribute('class', 'option-active')
    frees.setAttribute('class', 'option-active')
  }
  // 질문
  else if (option_value == 1) {
    articles.setAttribute('class', 'option-active')
    frees.setAttribute('class', 'option-inactive')
  }
  // 자유
  else {
    articles.setAttribute('class', 'option-inactive')
    frees.setAttribute('class', 'option-active')
  }
})
document.querySelector('.down1').addEventListener('click', function (e) {
  const option_value = e.target.value
  const articlescomment = document.querySelector('#my-articles-comment')
  const freescomment = document.querySelector('#my-frees-comment')
  // 전체
  if (option_value == 3) {
    articlescomment.setAttribute('class', 'option-active')
    freescomment.setAttribute('class', 'option-active')
  }
  // 질문
  else if (option_value == 4) {
    articlescomment.setAttribute('class', 'option-active')
    freescomment.setAttribute('class', 'option-inactive')
  }
  // 자유
  else {
    articlescomment.setAttribute('class', 'option-inactive')
    freescomment.setAttribute('class', 'option-active')
  }
})


// 팔로우 기능
const followBtn = document.querySelector('#follow-btn')

// 버튼을 클릭하면
followBtn.addEventListener('click', function (event) {
  // 팔로우 할 유저 아이디를 불러옴
  axios({
    method: 'get',
    url: `/accounts/${event.target.dataset.userId}/follow/`
  })
    .then(response => {
      // 응답 데이터를 출력함
      console.log(response.data)
      // 만약에 팔로우 상태일 경우
      if (response.data.isFollowing === true) {
        // 팔로우 취소 버튼을 위임하고
        event.target.classList.add('unfollow-button')
        followBtn.innerText = '팔로우 취소'
        // 팔로우 버튼을 없앰
        event.target.classList.remove('follow-button')
        // 팔로우 상태가 아닐 경우
      } else {
        // 팔로우 버튼을 위임하고
        event.target.classList.add('follow-button')
        followBtn.innerText = '팔로우'
        // 팔로우 취소 버튼을 없앰
        event.target.classList.remove('unfollow-button')
      }

      // 팔로우 숫자 변수 설정하고
      const followCnt = document.querySelector('#follow-cnt')
      // html에 나타내도록 함
      followCnt.innerHTML = `
            <style>
            .follower {
                margin-right: 2rem;
            }
            
            .follow-count {
                font-weight: 700;
            }
            </style>
            <p class="follower">팔로워 <span class="follow-count">${response.data.followers}</span></p>
            <p class="following">팔로잉 <span class="follow-count">${response.data.followings}</span></p>
          `
    })
})