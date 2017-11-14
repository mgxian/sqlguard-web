import fetch from '@/utils/fetch'

export function validatAlphabets(str) {
    const reg = /^[A-Za-z]+$/
    reg.test(str)
}

export function isUsernameCanRegister(str, callback) {
    fetch({
        url: 'users/' + str + '/check',
        method: 'get'
    }).then(response => {
        console.log(response)
        callback()
        return true
    }).catch(error => {
        console.log(error)
        callback(new Error('用户名已存在'))
        return false
    })
}