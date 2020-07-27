import "@/typedef";

/**
 * Base class for all `Scheduler` classes.
 */
class Scheduler {
  /**
   * Technically an array that could contain either
   * `Schedule` or `Scheduler`, but the exposed methods
   * for both
   * @type {Scheduler[]}
   * @private
   */
  _schedules;

  /**
   *
   * @param {any[]} schedules
   */
  constructor(schedules = []) {
    this._schedules = schedules;
  }

  /**
   *
   * @param {CourseSection} section
   * @returns {boolean}
   */
  checkConflict(section) {}

  /**
   *
   * @param {Course} course
   */
  addCourse(course) {
    this._schedules.forEach((schedule) => schedule.addCourse(course));
  }

  /**
   *
   * @param {Course} course
   * @param {CourseSection} section
   */
  addCourseSection(course, section) {
    this._schedules.forEach((schedule) =>
      schedule.addCourseSection(course, section)
    );
  }

  /**
   *
   * @param {CourseSection} section
   */
  removeCourseSection(section) {
    this._schedules.forEach((schedule) =>
      schedule.removeCourseSection(section)
    );
  }

  /**
   *
   * @param {Course} course
   */
  removeAllCourseSections(course) {
    this._schedules.forEach((schedule) =>
      schedule.removeAllCourseSections(course)
    );
  }
}

export default Scheduler;
