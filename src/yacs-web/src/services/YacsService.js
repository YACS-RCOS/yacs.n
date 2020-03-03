import axios from 'axios';

const client = axios.create({
    baseURL: 'http://localhost:5000/api'
});


export const getCourses = () => client.get('/class');
export const getDepartments = () => client.get('/department');
export const getSubSemesters = () => client.get('/subsemester');
export const LogIn = () => client.get('/login');
export const SignUp = () => client.get('/singup');
