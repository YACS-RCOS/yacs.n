import {ElNotification} from "element-plus";

export const $notify = (msg, type='info') => {
    ElNotification({
        title: msg,
        type
    })
}