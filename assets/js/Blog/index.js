let btnsSavePost = document.querySelectorAll('[btnSavePost]')
for (let btn of btnsSavePost) {
    btn.addEventListener('click', function () {
        let state = this.getAttribute('state') || 'delete'
        toggleBtnSavePost(btn, state)
    })
}

function toggleBtnSavePost(btn, state) {
    if (state == 'save') {
        btn.setAttribute('state', 'delete')
        btn.classList.remove('post-saved')
        btn.classList.remove('post-saved-animation')
    } else {
        btn.setAttribute('state', 'save')
        btn.classList.add('post-saved')
        btn.classList.add('post-saved-animation')
    }
}

function actionSavePost(btn, id) {
    let urlSavePost = `/b/post/save/${id}`
    SendAjax(urlSavePost, {}, 'POST', function (response) {
        let status = response.status_code
        if (status == '200') {
            let state_action = response.status_action
            if (state_action == 'save') {
                toggleBtnSavePost(btn, 'delete')
            } else {
                toggleBtnSavePost(btn, 'save')
            }
        }else{
            ShowNotificationMessage(response.status_text,'Error')
        }
    })
}

let countLike = document.getElementById('countLike')
function actionLikePost(btn, id) {
    let urlLikePost = `/b/post/like/${id}`
    SendAjax(urlLikePost, {}, 'POST', function (response) {
        let status = response.status_code
        if (status == '200') {
            let state_action = response.status_action
            if (state_action == 'like') {
                countLike.innerText = parseInt(countLike.innerText) + 1
                toggleBtnLikePost(btn, 'unlike')
            } else {
                countLike.innerText = parseInt(countLike.innerText) - 1
                toggleBtnLikePost(btn, 'like')
            }
        }else{
            ShowNotificationMessage(response.status_text,'Error')
        }
    })
}


// let btnLikePost = document.getElementById('btnLikePost')
// btnLikePost.addEventListener('click', function () {
//     let state = this.getAttribute('state') || 'unlike'
//     toggleBtnLikePost(this, state)
// })

function toggleBtnLikePost(btn, state) {
    if (state == 'like') {
        btn.setAttribute('state', 'unlike')
        btn.classList.remove('post-liked')
    } else {
        btn.setAttribute('state', 'like')
        btn.classList.add('post-liked')
    }
}