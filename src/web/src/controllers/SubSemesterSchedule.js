import '@/typedef';

import store from '@/store';

import { ADD_COURSE_SECTION, ADD_SCHEDULE, REMOVE_COURSE_SECTION } from '@/store/mutations';
import { generateScheduleId } from '@/store/helpers';
import { SCHEDULE_CONFLICT_ERROR } from './Schedule';

/**
 * Manages schedules for subsemesters
 * Allows adding and removing Course sections
 */
class SubSemesterSchedule {
  /**
   * List of schedules, each with a corresponding subsemester
   * in `scheduleSubsemesters`
   * @type {number[]}
   */
  scheduleIds;
  /** @type {Subsemester[]} */
  scheduleSubsemesters;

  /**
   * Initializes `schedules` and `scheduleSubsemesters`
   */
  constructor(subsemesters = null) {
    this.scheduleIds = [];
    this.scheduleSubsemesters = [];

    if (subsemesters) {
      subsemesters.forEach(s => this.addSubSemester(s));
    }
  }

  /**
   * Adds a new `Schedule` for `subsemester`
   * @param {Subsemester} subsemester
   */
  addSubSemester(subsemester) {
    const id = generateScheduleId();
    this.scheduleIds.push(id);
    store.commit(ADD_SCHEDULE, { id });
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
   * Adds `section` to the appropriate schedule(s) based on the duration of `course`
   * @param {Course} course
   * @param {CourseSection} section
   * @throws Will throw an error if there is a schedule conflict.
   * Error will include the subsemester
   */
  _addCourseSection(section) {
    const course = store.getters.getCourse(section.courseId);
    /** @type {Object<number, number>} */
    const scheduleSessionIndices = {};
    // Iterate through all schedules
    // If course spans a schedule's subsemester, then check all
    // the sessions of the selected section for schedule conflicts
    for (const [index, scheduleId] of this.scheduleIds.entries()) {
      if (this.withinCourseDuration(course, this.scheduleSubsemesters[index])) {
        try {
          /**
           * Store results of schedule conflict checking to use when
           * actually adding `section` to the schedule
           * @type {number[]}
           */
          const sessionIndices = [];
          for (const session of store.getters.getCourseSessions(section.sessionIds)) {
            sessionIndices.push(
              store.getters.getSchedule(scheduleId).getAddCourseSessionIndex(session)
            );
          }
          // Associate results with a schedule by `index`
          scheduleSessionIndices[index] = sessionIndices;
        } catch (err) {
          if (err.type === SCHEDULE_CONFLICT_ERROR) {
            err.subsemester = this.scheduleSubsemesters[index];
            err.message += ` in ${err.subsemester.display_string}`;
            throw err;
          }
          console.error(err);
        }
      }
    }

    // If there are no schedule conflicts, add the sessions to the appropriate schedules
    Object.entries(scheduleSessionIndices).forEach(([scheduleIndex, sessionIndices]) => {
      store.commit(ADD_COURSE_SECTION, {
        scheduleId: this.scheduleIds[scheduleIndex],
        sectionId: section.id,
        sessionIndices
      });
    });
  }

  /**
   * Remove all sessions of `section` from all schedules
   * @param {number} sectionId
   */
  _removeCourseSection(sectionId) {
    this.scheduleIds.forEach(scheduleId =>
      store.commit(REMOVE_COURSE_SECTION, { scheduleId, sectionId })
    );
  }

  /**
   * Remove all sessions of sections of `course` from all schedules
   * @param {number} courseId
   */
  _removeAllCourseSections(courseId) {
    this.scheduleIds.forEach(scheduleId =>
      store.commit(REMOVE_COURSE_SECTION, { scheduleId, courseId })
    );
  }
}

export default SubSemesterSchedule;
