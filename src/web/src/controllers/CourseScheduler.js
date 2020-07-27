import "@/typedef";

import Scheduler from "./Scheduler";

class CourseScheduler extends Scheduler {
  /** @type {Schedule[]} */
  schedules;

  /** @type {Course[]} */
  courses;

  constructor() {
    super();
    this.courses = [];
  }

  addCourse(course) {}

  addCourseSection(course, section) {}

  removeCourseSection(section) {}

  removeAllCourseSections(course) {}
}

export default CourseScheduler;
