import axios from "axios";

const client = axios.create({
    baseURL: '/api',
})

client.interceptors.request.use((config) => {
    return config
}, (error) => {
    console.log(error)
    return Promise.reject(error)
})
client.interceptors.response.use((response) => {
    return response.data
}, (error) => {
    return Promise.reject(error)
})

export default client