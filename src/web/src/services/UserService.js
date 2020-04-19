import axios from 'axios';

const client = axios.create({
  baseURL: '/api'
});

export const login = (userInfo) => client.post('/session', userInfo);

export const signup = (userInfo) => {
  return client.post('/user', userInfo);
}

export const logout = sessionId => client.delete('/session', {
  data: {
    "sessionID": sessionId
  },
  headers: {
    "Content-Type": "application/json"
  }
});