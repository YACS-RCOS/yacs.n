import axios, { AxiosResponse } from "axios";

const client = axios.create({
    baseURL: '/api',
    timeout: 30000
})

client.interceptors.request.use((config) => {
    return config
}, (reason) => {
    console.warn(`request failed because ${reason}`)
})

client.interceptors.response.use((res) => {
    return res.data
}, (err) => {
    console.warn(err)
})

export default client