import axios from 'axios';

const client = axios.create({
    baseURL: 'http://localhost:5000/api'
});

export const uploadCsv = (formData) => client.post("/bulkCourseUpload", formData);