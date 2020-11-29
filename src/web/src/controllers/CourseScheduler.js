import "@/typedef";

import Scheduler from "./Scheduler";

/**
 * The CourseScheduler class has two invariants:
 * 1. Every schedule contains exactly one course section from each course
 * in `courses`
 * 2. No two schedules contain the same set of course sections
 *
 * Given a set of courses, the CourseScheduler should build a set
 * of possible schedules for all non-conflicting course sections.
 *
 * When we add a course, we first try to add it to every schedule
 */
class CourseScheduler extends Scheduler {
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
