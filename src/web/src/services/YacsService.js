import "@/typedef";

import axios from "axios";

import { localToUTCDate, readableDate } from "@/utils";

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
 * NOTE: In The Case Course Listings Have Random Spaces In The Future,
 * This Is Likely Due To Two Course Objects Having The Same Identifier.
 * Thus, Should Revise The Following Code, If Necessary.
 */
export const _getCourseIdentifier = (courseObj) => {
  return `
    ${courseObj.crn}
    ${courseObj.name}
    ${courseObj.title}
    ${courseObj.min_credits}
    ${courseObj.max_credits}
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

export const newGetCourses = (semester, search = null) =>
  client.get("/class", { params: { semester, search } });

const parseSession = (sessions) => {
  let ret = [0, 0, 0, 0, 0];
  try {
    sessions.forEach((session) => {
      let a = session["time_start"].split(":").map((a) => Number.parseInt(a));
      let b = session["time_end"].split(":").map((a) => Number.parseInt(a));
      const duration = Math.abs(
        (b[0] - a[0]) * 2 + (a[1] < 30 ? 1 : 0) + (b[1] >= 30 ? 1 : 0)
      );
      const end = (20 - b[0]) * 2 + (b[1] < 30 ? 1 : 0);
      // generate 1 in bits for duration
      let ss = (1 << duration) - 1;
      // placeholder for day of week
      ss <<= end;
      ret[session["day_of_week"]] |= ss;
    });
  } catch (e) {
    return [0, 0, 0, 0, 0];
  }
  return ret;
};
/**
 * Returns a list of all courses
 * @returns {Promise<Course[]>}
 */
export const getCourses = (semester, search = null, filter = true) =>
  client.get("/class", { params: { semester, search } }).then(({ data }) => {
    let courses = data.map((c) => {
      c.date_start = localToUTCDate(new Date(c.date_start));
      c.date_end = localToUTCDate(new Date(c.date_end));

      // Filter out sections that are null
      c.sections = c.sections.filter((s) => !!s);
      // Initialize section.selected to false
      c.sections.forEach((s) => {
        if (s) s.selected = false;
        s.title = c.title;
        s.date_start = c.date_start;
        s.date_end = c.date_end;
        s.times = parseSession(s.sessions);
      });
      // Initialize course.selected to false
      c.selected = false;
      // Generate id based on course content
      c.id = _getCourseIdentifier(c);

      c.vscrl_type = c.description ? "with-info" : "without-info";
      return c;
    });
    return filter ? courses.filter((c) => c.sections.length !== 0) : courses;
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
  client.post("/user/course", course_info).then(({ data }) => {
    return data;
  });

export const removeStudentCourse = (course_info) =>
  client
    .delete("/user/course", {
      data: course_info,
    })
    .then((res) => res.data);

export const getStudentCourses = () =>
  client.get("/user/course").then((res) => res.data);

export const getProfessors = () =>
  client.get("/professor").then((res) => res.data);


export const addProfessors = () =>
  client.post("/professor/add").then((res) => res.data);

export const addProfessorsTest = () =>
  client.post("/professor/add/test").then((res) => res.data);
