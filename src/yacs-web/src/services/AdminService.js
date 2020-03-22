import axios from 'axios';

const client = axios.create({
  baseURL: '/api'
});

export const uploadCsv = formData => client.post('/bulkCourseUpload', formData);

export const updateSemester = sem => client.post('/defaultsemester', sem);

export const getSemester = () => client.get('/defaultsemester');