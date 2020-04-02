import axios from 'axios';

const client = axios.create({
  baseURL: '/api'
});

export const login = userInfo => client.post('/session', userInfo);