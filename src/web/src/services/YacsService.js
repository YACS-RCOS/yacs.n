import '@/typedef';

import axios from 'axios';

import { readableDate, localToUTCDate } from '@/utils';

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
 * @private
 */
const _getCourseIdentifier = courseObj =>
  [
    courseObj.title,
    courseObj.department,
    courseObj.level,
    courseObj.date_start.getMonth() + 1,
    courseObj.date_start.getDay() + 1,
    courseObj.date_start.getFullYear(),
    courseObj.date_end.getMonth() + 1,
    courseObj.date_end.getDay() + 1,
    courseObj.date_end.getFullYear()
  ].join('|');

/**
 * Returns unique identifier for course section
 * @param {CourseSection} section
 */
const _getCourseSectionIdentifier = section => `${section.crn}`;

/**
 * Returns unique identifier for course session
 * @param {CourseSession} session
 */
const _getCourseSessionIdentifier = session =>
  [session.crn, session.day_of_week, session.time_start, session.time_end].join('|');

/**
 * Returns a list of all courses
 * @returns {Promise<Course[]>}
 */
export const getCourses = () =>
  client.get('/class').then(({ data }) => {
    return data.map(course => {
      course.date_start = localToUTCDate(new Date(course.date_start));
      course.date_end = localToUTCDate(new Date(course.date_end));

      // Generate id based on course content
      course.id = _getCourseIdentifier(course);
      // Filter out sections that are null
      course.sections = course.sections.filter(s => !!s);
      course.sections.forEach(section => {
        section.id = _getCourseSectionIdentifier(section);
        section.courseId = course.id;

        section.selected = false; // Initialize section.selected to false

        section.sessions.forEach(session => {
          session.id = _getCourseSessionIdentifier(session);
          session.courseId = course.id;
          session.sectionId = section.id;
        });
      });
      // Initialize course.selected to false
      course.selected = false;

      return course;
    });
  });
/**
 * Returns a list of all departments
 * @returns {Promise<Department[]>}
 */
export const getDepartments = () => client.get('/department').then(({ data }) => data);
/**
 * Returns a list of all subsemesters
 * @returns {Promise<Subsemester[]>}
 */
export const getSubSemesters = () =>
  client.get('/subsemester').then(({ data }) => {
    return data.map(subsemester => {
      subsemester.date_start = localToUTCDate(new Date(subsemester.date_start));
      subsemester.date_end = localToUTCDate(new Date(subsemester.date_end));
      subsemester.date_start_display = readableDate(subsemester.date_start);
      subsemester.date_end_display = readableDate(subsemester.date_end);
      // Used to determine what semester the subsemester is part of
      subsemester.semester_name = subsemester.parent_semester_name;
      subsemester.display_string = subsemester.semester_part_name
        ? subsemester.semester_part_name
        : `${subsemester.date_start_display} - ${subsemester.date_end_display}`;

      return subsemester;
    });
  });
