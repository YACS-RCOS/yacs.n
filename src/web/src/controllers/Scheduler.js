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
   * @protected
   */
  schedules;

  /**
   *
   * @param {Scheduler[]} schedules
   */
  constructor(schedules = []) {
    this.schedules = schedules;
  }

  /**
   *
   * @param {CourseSection} section
   * @returns {boolean}
   */
  checkConflict(section) {
    return this.schedules.some((schedule) => schedule.checkConflict(section));
  }

  /**
   *
   * @param {Course} course
   */
  addCourse(course) {
    this.schedules.forEach((schedule) => schedule.addCourse(course));
  }

  /**
   *
   * @param {Course} course
   * @param {CourseSection} section
   */
  addCourseSection(course, section) {
    this.schedules.forEach((schedule) =>
      schedule.addCourseSection(course, section)
    );
  }

  /**
   * @param {Course} course
   * @param {CourseSection} section
   */
  removeCourseSection(course, section) {
    this.schedules.forEach((schedule) =>
      schedule.removeCourseSection(course, section)
    );
  }

  /**
   *
   * @param {Course} course
   */
  removeAllCourseSections(course) {
    this.schedules.forEach((schedule) =>
      schedule.removeAllCourseSections(course)
    );
  }
}

export default Scheduler;
