/**
 * @typedef CourseSession
 * @property {string} crn
 * @property {number} day_of_week
 * @property {string} section
 * @property {string} semester
 * @property {string} time_end
 * @property {string} time_start
 * @property {string} id
 * @property {string} sectionId
 * @property {string} courseId
 */

/**
 * @typedef CourseSection
 * @property {string} crn
 * @property {string} department
 * @property {number} level
 * @property {string} semester
 * @property {CourseSession[]} sessions
 * @property {string} id
 * @property {string} courseId
 * @property {boolean} selected
 */
/**
 * @typedef Course
 * @property {string} department
 * @property {number} level
 * @property {CourseSection[]} sections
 * @property {string} title
 * @property {Date} date_start
 * @property {Date} date_end
 * @property {string} id
 * @property {boolean} selected
 */
/**
 * @typedef Subsemester
 * @property {Date} date_start
 * @property {Date} date_end
 * @property {string} date_start_display
 * @property {string} date_end_display
 * @property {string} semester_name
 * @property {string} display_string
 */
/**
 * @typedef Department
 * @property {string} department
 */
