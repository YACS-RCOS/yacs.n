import axios from 'axios';

import Vue from 'vue';

const client = axios.create({
  baseURL: '/api'
});

const DURATION_TO_CONSIDER_REQUESTS_IN_SAME_BLOCK = 1000;

client.interceptors.request.use((config) => {
  Vue.prototype.nstate.currentRequests += 1;
  Vue.prototype.nstate.currentRequestsInFlight += 1;
  if (Vue.prototype.nstate.timer) {
    clearTimeout(Vue.prototype.nstate.timer);
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

client.interceptors.response.use((config) => {
  Vue.prototype.nstate.currentResponses += 1;
  Vue.prototype.nstate.timer = setTimeout(() => {
    Vue.prototype.nstate.timeoutExpired = true;
  }, DURATION_TO_CONSIDER_REQUESTS_IN_SAME_BLOCK);
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const uploadCsv = formData => client.post('/bulkCourseUpload', formData);

export const mapDateRangeToSemesterPart = formData => client.post('/mapDateRangeToSemesterPart', formData);
