import axios from 'axios';

import { readableDate } from '@/utils';

const client = axios.create({
    baseURL: 'http://localhost:5000/api'
});


const _getCourseIdentifier = (courseObj) => {
    return `${courseObj.department}${courseObj.level}${courseObj.date_start.getMonth() + 1}${courseObj.date_start.getDay() + 1}${courseObj.date_start.getFullYear()}${courseObj.date_end.getMonth() + 1}${courseObj.date_end.getDay() + 1}${courseObj.date_end.getFullYear()}`;
}

export const getCourses = () => client.get('/class').then(({ data }) => {
    return data.map(c => {
        c.date_start = new Date(c.date_start);
        c.date_end = new Date(c.date_end);
  
        c.sections = c.sections.filter(s => !!s);
        c.sections.forEach(s => {if (s) s.selected = false;});
        c.selected = false;
        c.id = _getCourseIdentifier(c);
        return c;
    });
});
export const getDepartments = () => client.get('/department').then(({ data }) => {
    return data;
});
export const getSubSemesters = () => client.get('/subsemester').then(({ data }) => {
    return data.map(subsemester => {
        subsemester.date_start = new Date(subsemester.date_start)
        subsemester.date_end = new Date(subsemester.date_end)
        subsemester.date_start_display = readableDate(subsemester.date_start);
        subsemester.date_end_display = readableDate(subsemester.date_end);

        subsemester.text = `${subsemester.date_start_display} - ${subsemester.date_end_display}`;


        return subsemester;
    });
});
