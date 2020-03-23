import axios from 'axios';

import Vue from 'vue';

const client = axios.create({
  baseURL: '/api'
});

client.interceptors.request.use((config) => {
  Vue.prototype.nstate.currentRequests += 1;
  Vue.prototype.nstate.currentRequestsInFlight += 1;
  return config;
}, (error) => {
  return Promise.reject(error);
});

client.interceptors.response.use((config) => {
  Vue.prototype.nstate.currentResponses += 1;
  console.log(Vue.prototype);
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const uploadCsv = formData => client.post('/bulkCourseUpload', formData);

export const mapDateRangeToSemesterPart = formData => client.post('/mapDateRangeToSemesterPart', formData);
