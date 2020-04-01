import '@/typedef';

import store from '@/store';

// eslint-disable-next-line no-unused-vars
import Schedule from '@/controllers/Schedule';
import { ADD_COURSE_SECTION, ADD_SCHEDULE, REMOVE_COURSE_SECTION } from '@/store/mutations';
import { generateScheduleId } from '@/store/helpers';

/**
 * Manages schedules for subsemesters
 * Allows adding and removing Course sections
 */
class SubSemesterScheduler {
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
      // store
      //   .dispatch(CREATE_SCHEDULE, { count: subsemesters.length })
      //   .then(ids => (this.scheduleIds = ids));
      // this.scheduleSubsemesters = subsemesters;
      subsemesters.forEach(s => this.addSubSemester(s));
    }
  }

  /**
   * Adds a new `Schedule` for `subsemester`
   * @param {Subsemester} subsemester
   */
  addSubSemester(subsemester) {
    // store.dispatch(CREATE_SCHEDULE).then(id => this.scheduleIds.push(id));
    // this.scheduleIds.push(store.dispatch(CREATE_SCHEDULE));
    const id = generateScheduleId();
    this.scheduleIds.push(id);
    store.commit(ADD_SCHEDULE, { id });
    // store.commit(ADD_SCHEDULE, { id: subsemester.display_string });
    // this.schedules.push(new Schedule());
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
  // addCourseSection(course, section) {
  _addCourseSection(section) {
    const course = store.getters.getCourse(section.courseId);
    /** @type {Object<number, number>} */
    const scheduleSessionIndices = {};
    // Iterate through all schedules
    // If course spans a schedule's subsemester, then check all
    // the sessions of the selected section for schedule conflicts
    // for (const [index, schedule] of store.getters.schedules.entries()) {
    // for (const [index, schedule] of this.schedules.entries()) {
    for (const [index, scheduleId] of this.scheduleIds.entries()) {
      if (this.withinCourseDuration(course, this.scheduleSubsemesters[index])) {
        try {
          /**
           * Store results of schedule conflict checking to use when
           * actually adding `section` to the schedule
           * @type {number[]}
           */
          const sessionIndices = [];
          // for (const session of section.sessions) {
          for (const session of store.getters.getSessions(section.sessionIds)) {
            // sessionIndices.push(schedule.getAddCourseSessionIndex(session));
            sessionIndices.push(
              store.getters.getSchedule(scheduleId).getAddCourseSessionIndex(session)
            );
          }
          // Associate results with a schedule by `index`
          scheduleSessionIndices[index] = sessionIndices;
        } catch (err) {
          if (err.type === 'Schedule Conflict') {
            err.subsemester = this.scheduleSubsemesters[index];
            console.log(err);
            throw err;
          }
          console.log(err);
        }
      }
    }

    // If there are no schedule conflicts, add the sessions to the appropriate schedules
    Object.entries(scheduleSessionIndices).forEach(([scheduleIndex, sessionIndices]) => {
      // store.getters.schedules[scheduleIndex].addCourseSection(course, section, sessionIndices);
      // this.schedules[scheduleIndex].addCourseSection(course, section, sessionIndices);
      store.commit(ADD_COURSE_SECTION, {
        scheduleId: this.scheduleIds[scheduleIndex],
        sectionId: section.id,
        sessionIndices
      });
    });
  }

  /**
   * Remove all sessions of `section` from all schedules
   * @param {CourseSection} section
   */
  _removeCourseSection(section) {
    // store.getters.schedules.forEach(s => s._removeCourseSection(section));
    // this.schedules.forEach(s => s.removeCourseSection(section));
    this.scheduleIds.forEach(scheduleId =>
      store.commit(REMOVE_COURSE_SECTION, { scheduleId, sectionId: section.id })
    );
  }

  /**
   * Remove all sessions of sections of `course` from all schedules
   * @param {Course} course
   */
  _removeAllCourseSections(course) {
    // store.getters.schedules.forEach(s => s.removeAllCourseSections(course));
    // store.getters.schedules.forEach(s => s.removeCourse(course));
    // this.schedules.forEach(s => s.removeCourse(course));
    this.scheduleIds.forEach(scheduleId =>
      store.commit(REMOVE_COURSE_SECTION, { scheduleId, courseId: course.id })
    );
  }
}

export default SubSemesterScheduler;
