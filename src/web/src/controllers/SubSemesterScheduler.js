import "@/typedef";

import Schedule from "@/controllers/Schedule";

/**
 * Manages schedules for subsemesters
 * Allows adding and removing Course sections
 */
class SubSemesterScheduler {
  /**
   * List of schedules, each with a corresponding subsemester
   * in `scheduleSubsemesters`
   * @type {Schedule[]}
   */
  schedules;
  /** @type {Subsemester[]} */
  scheduleSubsemesters;

  /**
   * Initializes `schedules` and `scheduleSubsemesters`
   */
  constructor() {
    this.schedules = [];
    this.scheduleSubsemesters = [];
  }

  /**
   * Adds a new `Schedule` for `subsemester`
   * @param {Subsemester} subsemester
   */
  addSubSemester(subsemester) {
    this.schedules.push(new Schedule());
    this.scheduleSubsemesters.push(subsemester);
  }

  /**
   * Checks whether `course` spans the entire duration of `subsemester`
   * @param {Course} course
   * @param {Subsemester} subsemester
   * @returns {boolean}
   */
  withinCourseDuration(course, subsemester) {
    return (
      course.date_start.getTime() <= subsemester.date_start.getTime() &&
      course.date_end.getTime() >= subsemester.date_end.getTime()
    );
  }

  /**
   * Adds record of selected class to all schedules
   * @param {Course} course
   */
  addCourse(course) {
    this.schedules.forEach((s) => s.addCourse(course));
  }

  /**
   * Adds `section` to the appropriate schedule(s) based on the duration of `course`
   * @param {Course} course
   * @param {CourseSection} section
   * @returns {boolean} true if course session is added, false if schedule conflict
   */
  addCourseSection(course, section) {
    /** @type {Object<number, number>} */
    const scheduleSessionIndices = {};
    // Iterate through all schedules
    // If course spans a schedule's subsemester, then check all
    // the sessions of the selected section for schedule conflicts
    for (const [index, schedule] of this.schedules.entries()) {
      if (this.withinCourseDuration(course, this.scheduleSubsemesters[index])) {
        /**
         * Store results of schedule conflict checking to use when
         * actually adding `section` to the schedule
         * @type {number[]}
         */
        const sessionIndices = [];
        for (const session of section.sessions) {
          const sessionIndex = schedule.getAddCourseSessionIndex(session);

          if (sessionIndex === null) {
            return false;
          }

          sessionIndices.push(sessionIndex);
        }
        // Associate results with a schedule by `index`
        scheduleSessionIndices[index] = sessionIndices;
      }
    }

    // If there are no schedule conflicts, add the sessions to the appropriate schedules
    Object.entries(scheduleSessionIndices).forEach(
      ([scheduleIndex, sessionIndices]) => {
        this.schedules[scheduleIndex].addCourseSection(
          course,
          section,
          sessionIndices
        );
      }
    );

    return true;
  }

  /**
   * Remove all sessions of `section` from all schedules
   * @param {CourseSection} section
   */
  removeCourseSection(section) {
    this.schedules.forEach((s) => s.removeCourseSection(section));
  }

  /**
   * Remove all sessions of sections of `course` from all schedules
   * @param {Course} course
   */
  removeAllCourseSections(course) {
    this.schedules.forEach((s) => s.removeCourse(course));
  }
}

export default SubSemesterScheduler;
