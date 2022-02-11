import {reactive, ref, effect} from 'vue';

export default function LocalStorage(key, defaultValue){
    let data = reactive({});

    Object.assign(data, localStorage[key] && JSON.parse(localStorage[key]) || defaultValue);

    effect(() => localStorage[key] = JSON.stringify(data));

    return data;
}

export const localRef = (key, defaultValue) => {
    let data = ref(defaultValue);

    data.value = Object.assign(data.value, localStorage[key] && JSON.parse(localStorage[key]) || defaultValue);

    effect(() => localStorage[key] = JSON.stringify(data.value));

    return data;
}