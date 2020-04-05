import '@/typedef';

import store from '@/store';

export const SCHEDULE_CONFLICT_ERROR = 'Schedule Conflict';
// Internal errors
const INVALID_SESSION_INDICES_ERROR = 'Invalid Session Indices';
const NULL_SESSION_INDEX_ERROR = 'Null Session Index';

/**
 * Holds the `CourseSession`s for a weekly schedule
 * Can add/remove course sessions and determine if there is a schedule conflict
 */
class Schedule {
  static SCHEDULE_DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr'];
  // hours indicate start (inclusive) of one hour block with exclusive end e.g. [8, 9) in ascending order
  static SCHEDULE_HOURS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
  static SCHEDULE_DAY_DURATION =
    Schedule.SCHEDULE_HOURS[Schedule.SCHEDULE_HOURS.length - 1] - Schedule.SCHEDULE_HOURS[0];

  /**
   * Each sub array contains the `CourseSession`s for the corresponding entry in `SCHEDULE_DAYS`
   * e.g. `dailySessions[1]` would return the `CourseSession`s on Tuesday
   * Within each sub array, the `CourseSession`s are ordered by start time
   * @type {Array<CourseSession[]>}
   */
  dailySessions;

  /**
   * Create a new `Schedule`
   * Initializes `dailySessions`
   */
  constructor() {
    this.dailySessions = [];

    for (let d = 0; d < Schedule.SCHEDULE_DAYS.length; d++) {
      this.dailySessions.push([]);
    }
  }

  /**
   * Returns the index that newCourseSession should be inserted at or `null` if there
   * is a schedule conflict
   * Assumes that `newCourseSession.time_start != newCourseSession.time_end`
   * @param {CourseSession} newCourseSession
   * @returns {number|null} the index to insert the new course session
   * @throws Will throw error if `newCourseSession` conflicts with existing sessions
   */
  getAddCourseSessionIndex(newCourseSession) {
    const daySessions = this.dailySessions[newCourseSession.day_of_week];
    const numSessions = daySessions.length;

    // If daySessions is empty, no conflicts
    if (numSessions === 0) return 0;

    // If session is after latest session, return last index
    if (
      newCourseSession.time_start >= daySessions[numSessions - 1].time_end &&
      newCourseSession.time_end > daySessions[numSessions - 1].time_end
    ) {
      return numSessions;
    }

    // Check courseSessions in the same day as newCourseSession for conflicts
    for (let i = 0; i < daySessions.length; i++) {
      let sess = daySessions[i];

      // If newCourseSession time block is before sess time block return current index
      if (
        newCourseSession.time_end <= sess.time_start &&
        newCourseSession.time_start < sess.time_start
      ) {
        return i;

        // If newCourseSession time block is after sess time block
      } else if (
        newCourseSession.time_start >= sess.time_end &&
        newCourseSession.time_end > sess.time_end
      ) {
        // Check next courseSession
        continue;

        // Otherwise there is a schedule conflict
      } else {
        throw {
          type: SCHEDULE_CONFLICT_ERROR,
          existingSession: sess,
          addingSession: newCourseSession,
          message: `
            Schedule conflict between 
            ${newCourseSession.id} 
            and ${sess.id}
        `
        };
      }
    }

    // Should be unreachable
    return null;
  }

  /**
   * Removes a `courseSession` from this schedule by iterating
   * through `dailySessions`
   * Definitely a better way to do this but this works for now
   * @param {CourseSession} courseSession
   * @returns {boolean} if course session was removed from schedule
   */
  _removeCourseSession(courseSession) {
    const index = this.dailySessions[courseSession.day_of_week].findIndex(
      cs => cs.id === courseSession.id
    );

    if (index === -1) return false;

    // This should always return true
    return this.dailySessions[courseSession.day_of_week].splice(index, 1).length > 0;
  }

  /**
   * Adds all the `CourseSession`s in `courseSection` to this schedule
   * @param {CourseSection} courseSection
   * @param {Course} course
   * @param {number[]} [sessionIndices=null] If schedule conflict has already been checked, pass
   * the resultant indices in to avoid rechecking
   * @returns {boolean} if course section was added to schedule
   * @throws Will throw error if `newCourseSession` conflicts with existing sessions
   */
  _addCourseSection(courseSection, sessionIndices = null) {
    if (!!sessionIndices && sessionIndices.length != courseSection.sessionIds.length) {
      throw {
        type: INVALID_SESSION_INDICES_ERROR,
        message: `Provided number of checked conflicts ${sessionIndices.length} 
                            does not match number of sessions ${courseSection.sessionIds.length}, 
                            ignoring..`
      };
    }
    /**
     * @private
     * @typedef Addition
     * @property {number} index
     * @property {number} day
     * @property {CourseSession} courseSession
     */
    /**
     * Keeps track of the courseSessions that will be added
     * We need this in case we are inserting adjacent sessions
     * @type {Addition[]}
     * @private
     */
    const additions = [];

    // Check that there are no session conflicts in course section sessions
    // courseSection.sessions.forEach((courseSession, index) => {
    store.getters.getCourseSessions(courseSection.sessionIds).forEach((courseSession, index) => {
      const sessionIndex = sessionIndices?.[index] ?? this.getAddCourseSessionIndex(courseSession); // If already checked for conflicts use provided indices

      if (sessionIndex === null) {
        throw {
          type: NULL_SESSION_INDEX_ERROR,
          message: 'The unthinkable hath occureth'
        };
      } else {
        additions.push({
          index: sessionIndex,
          day: courseSession.day_of_week,
          courseSession
        });
      }
    });

    additions.sort(
      (a1, a2) => a1.day - a2.day || a2.courseSession.time_start - a1.courseSession.time_start
    );
    for (const { index, day, courseSession } of additions) {
      this.dailySessions[day].splice(index, 0, courseSession);
    }

    return true;
  }

  /**
   * Remove all sessions in courseSection from schedule
   * Does not check if individual course session removal succeeds
   * @param {number} sectionId
   */
  _removeCourseSection(sectionId) {
    const courseSection = store.getters.getCourseSection(sectionId);
    for (const courseSession of store.getters.getCourseSessions(courseSection.sessionIds)) {
      this._removeCourseSession(courseSession);
    }
  }

  /**
   * Removes all sections of course
   * @param {number} courseId
   */
  _removeAllCourseSections(courseId) {
    store.getters.getCourse(courseId).sectionIds.forEach(id => this._removeCourseSection(id));
  }
}

export default Schedule;
