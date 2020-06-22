import "@/typedef";

import axios from "axios";

import { readableDate, localToUTCDate } from "@/utils";

const client = axios.create({
  baseURL: "/api",
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
const _getCourseIdentifier = (courseObj) => {
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
export const getCourses = (semester) =>
  client
    .get("/class", {
      params: {
        semester: semester,
      },
    })
    .then(({ data }) => {
      return data.map((c) => {
        c.date_start = localToUTCDate(new Date(c.date_start));
        c.date_end = localToUTCDate(new Date(c.date_end));

        // Filter out sections that are null
        c.sections = c.sections.filter((s) => !!s);
        // Initialize section.selected to false
        c.sections.forEach((s) => {
          if (s) s.selected = false;
        });
        // Initialize course.selected to false
        c.selected = false;
        // Generate id based on course content
        c.id = _getCourseIdentifier(c);

        c.vscrl_type = c.description ? "with-info" : "without-info";
        return c;
      });
    });
/**
 * Returns a list of all departments
 * @returns {Promise<Department>}
 */
export const getDepartments = () =>
  client.get("/department").then(({ data }) => {
    return data;
  });
/**
 * Returns a list of all subsemesters
 * @returns {Promise<Subsemester[]>}
 */
export const getSubSemesters = (semester) =>
  client
    .get("/subsemester", {
      params: {
        semester: semester,
      },
    })
    .then(({ data }) => {
      return data.map((subsemester) => {
        subsemester.date_start = localToUTCDate(
          new Date(subsemester.date_start)
        );
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

export const getSemesters = () =>
  client.get("/semester").then((res) => res.data);

export const addStudentCourse = (course_info) =>
  client.post("/course", course_info).then(({ data }) => {
    return data;
  });

export const removeStudentCourse = (course_info) =>
  client
    .delete("/course", {
      data: course_info,
    })
    .then((res) => res.data);

export const getStudentCourses = (user_info) =>
  client
    .get("/course", {
      params: user_info,
    })
    .then((res) => res.data);

export const getCoursesBySearch = (semester, search) =>
    client
      .get("/search", {
        params: {
          semester: semester,
          search: search,
        },
      })
      .then(({ data }) => {
        return data.map((c) => {
          c.date_start = localToUTCDate(new Date(c.date_start));
          c.date_end = localToUTCDate(new Date(c.date_end));
  
          // Filter out sections that are null
          c.sections = c.sections.filter((s) => !!s);
          // Initialize section.selected to false
          c.sections.forEach((s) => {
            if (s) s.selected = false;
          });
          // Initialize course.selected to false
          c.selected = false;
          // Generate id based on course content
          c.id = _getCourseIdentifier(c);
  
          c.vscrl_type = c.description ? "with-info" : "without-info";
          return c;
        });
      });
