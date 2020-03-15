import axios from 'axios';

const client = axios.create({
  baseURL: '/api'
});

export const uploadCsv = formData => client.post('/bulkCourseUpload', formData);
