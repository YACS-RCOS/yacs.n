import axios from 'axios';

const client = axios.create({
  baseURL: '/api'
});

export const uploadCsv = formData => client.post('/bulkCourseUpload', formData);

export const mapDateRangeToSemesterPart = formData => client.post('/mapDateRangeToSemesterPart', formData);

export const updateSemester = semester => client.post('/defaultsemesterset', {'default': semester});

export const getSemester = () => client.get('/defaultsemester').then(({ data }) => {
    																return data;
  																});

