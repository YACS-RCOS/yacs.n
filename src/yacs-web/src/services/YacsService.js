import '@/typedef';

import axios from 'axios';

import { readableDate } from '@/utils';

const client = axios.create({
  baseURL: '/api'
});

/**
 * Accesses the YACS API
 * @module YacsService
 */

/**
 * Returns the unique identifier for a course. Modeled after the primary key in the database for
 * a course.
 * @param {Course} courseObj an object that is a subclass of course
 * @returns {string} the unique identifier of a course
 */
const _getCourseIdentifier = courseObj => {
  return `
    ${courseObj.department}
    ${courseObj.level}
    ${courseObj.date_start.getMonth() + 1}
    ${courseObj.date_start.getDay() + 1}
    ${courseObj.date_start.getFullYear()}
    ${courseObj.date_end.getMonth() + 1}
    ${courseObj.date_end.getDay() + 1}
    ${courseObj.date_end.getFullYear()}
  `;
};

/**
 * Returns a list of all courses
 * @returns {Promise<Course[]>}
 */
export const getCourses = () =>
  client.get('/class').then(({ data }) => {
    return data.map(c => {
      c.date_start = new Date(c.date_start);
      c.date_end = new Date(c.date_end);

      // Filter out sections that are null
      c.sections = c.sections.filter(s => !!s);
      // Initialize section.selected to false
      c.sections.forEach(s => {
        if (s) s.selected = false;
      });
      // Initialize course.selected to false
      c.selected = false;
      // Generate id based on course content
      c.id = _getCourseIdentifier(c);
      return c;
    });
  });
/**
 * Returns a list of all departments
 * @returns {Promise<Department>}
 */
export const getDepartments = () =>
  client.get('/department').then(({ data }) => {
    return data;
  });
/**
 * Returns a list of all subsemesters
 * @returns {Promise<Subsemester[]>}
 */
export const getSubSemesters = () =>
  client.get('/subsemester').then(({ data }) => {
    return data.map(subsemester => {
      console.log(subsemester.date_start);
      subsemester.date_start = new Date(subsemester.date_start);
      subsemester.date_end = new Date(subsemester.date_end);
      // JS dates will auto convert your passed in date string to
      // the local timezone. So, when the server gives back semester end date of Aug 21st 00:00:00 GMT,
      // in EST it becomes Aug 20th 20:00:00, where the timezone difference between EST and UTC is 4 hours.
      // Could either change the date type in the course table to timezone and set its time to midnight,
      // or this, which is offset the auto-converted local datetime by the 4 hours.
      subsemester.date_start.setUTCHours(subsemester.date_start.getUTCHours() + subsemester.date_start.getTimezoneOffset()/60);
      subsemester.date_end.setUTCHours(subsemester.date_end.getUTCHours() + subsemester.date_end.getTimezoneOffset()/60);
      subsemester.date_start_display = readableDate(subsemester.date_start);
      subsemester.date_end_display = readableDate(subsemester.date_end);
      // Used to determine what semester the subsemester is part of
      subsemester.semester_name = subsemester.parent_semester_name;
      subsemester.display_string = subsemester.semester_part_name ? subsemester.semester_part_name : `${subsemester.date_start_display} - ${subsemester.date_end_display}`;

      return subsemester;
    });
  });
