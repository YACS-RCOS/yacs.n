import "@/typedef";
import Scheduler from "./Scheduler";

/**
 * Holds the `CourseSession`s for a weekly schedule
 * Can add/remove course sessions and determine if there is a schedule conflict
 */
class Schedule extends Scheduler {
  static SCHEDULE_DAYS = ["Mo", "Tu", "We", "Th", "Fr"];
  // hours indicate start (inclusive) of one hour block with exclusive end e.g. [8, 9) in ascending order
  static SCHEDULE_HOURS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
  static SCHEDULE_DAY_DURATION =
    Schedule.SCHEDULE_HOURS[Schedule.SCHEDULE_HOURS.length - 1] -
    Schedule.SCHEDULE_HOURS[0];

  /**
   * Each sub array contains the `CourseSession`s for the corresponding entry in `SCHEDULE_DAYS`
   * e.g. `dailySessions[1]` would return the `CourseSession`s on Tuesday
   * Within each sub array, the `CourseSession`s are ordered by start time
   * @type {Array<CourseSession[]>}
   */
  dailySessions;

  /**
   * Array containing the selected CourseSessions matching data stored in dailySessions
   * Allowing identification and tracing values to access department and level
   * by matching the crn from a CourseSession to its CourseSection
   * @type {Array<CourseSection>}
   */
  selectedSections;

  /**
   * Array containing the selected Courses matching data stored in selectedSections
   * Allowing identification and tracing values to access course title and professors
   * by matching the department and level from a CourseSection to its Course
   * @type {Array<Course>}
   */
  selectedCourses;

  /**
   * Create a new `Schedule`
   * Initializes `dailySessions,' 'selectedSections,' and 'selectedCourses'
   */
  constructor() {
    super();

    this.dailySessions = [];
    this.selectedSections = [];
    this.selectedCourses = [];

    for (let d = 0; d < Schedule.SCHEDULE_DAYS.length; d++) {
      this.dailySessions.push([]);
    }
  }

  /**
   * Wrapper around `getAddCourseSessionIndex`
   * @param {CourseSection} courseSection
   * @returns {boolean} whether courseSection has conflict with schedule
   */
  hasConflict(courseSection) {
    for (let session of courseSection.sessions) {
      if (this.getAddCourseSessionIndex(session) === null) {
        return false;
      }
    }

    return true;
  }

  /**
   *
   * @param {CourseSection} courseSection
   * @returns {boolean}
   */
  checkConflict(courseSection) {
    return this.hasConflict(courseSection);
  }

  /**
   * Returns the index that newCourseSession should be inserted at or `null` if there
   * is a schedule conflict
   * Assumes that `newCourseSession.time_start != newCourseSession.time_end`
   * @param {CourseSession} newCourseSession
   * @returns {number|null} the index to insert the new course session or null if there
   * is a schedule conflict
   */
  getAddCourseSessionIndex(newCourseSession) {
    if (!newCourseSession) {
      console.warn(`Ignoring add null/undefined courseSession`);
    } else if (
      newCourseSession.day_of_week === undefined ||
      newCourseSession.time_end === undefined ||
      newCourseSession.time_start === undefined
    ) {
      console.error(`
        Cannot add courseSession with undefined values
        ${JSON.stringify(newCourseSession)}
      `);
    } else {
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
          console.error(`
              Schedule conflict between
              ${JSON.stringify(newCourseSession)}
              and ${JSON.stringify(sess)}
          `);
          break;
        }
      }

      // Schedule conflict
      return null;
    }
  }

  /**
   * Removes a `courseSession` from this schedule by iterating
   * through `dailySessions`
   * Definitely a better way to do this but this works for now
   * @param {CourseSession} courseSession
   * @returns {boolean} if course session was removed from schedule
   */
  _removeCourseSession(courseSession) {
    if (!courseSession) {
      console.warn(`Ignoring remove null/undefined courseSession`);
    } else {
      let i = 0;
      for (const sess of this.dailySessions[courseSession.day_of_week]) {
        if (
          sess.crn === courseSession.crn &&
          sess.section === courseSession.section &&
          sess.time_start === courseSession.time_start &&
          sess.time_end === courseSession.time_end &&
          sess.day_of_week === courseSession.day_of_week
        ) {
          this.dailySessions[courseSession.day_of_week].splice(i, 1);
          console.log(`Removed courseSession at index ${i}`);
          return true;
        }
        i += 1;
      }

      // console.error(`Failed to remove could not find ${JSON.stringify(courseSession)}`);
      return false;
    }
  }

  /**
   * Adds all the `CourseSession`s in `courseSection` to this schedule
   * @param {CourseSection} courseSection
   * @param {Course} course
   * @param {number[]} [sessionIndices=null] If schedule conflict has already been checked, pass
   * the resultant indices in to avoid rechecking
   * @returns {boolean} true if course section was added to schedule, false if schedule conflict
   */
  addCourseSection(course, courseSection, sessionIndices = null) {
    if (!courseSection) {
      console.warn(`Ignoring add null/undefined courseSection`);
    } else if (courseSection.sessions.length === 0) {
      console.error(
        `Cannot add courseSection with no sessions ${JSON.stringify(
          courseSection
        )}`
      );
    } else if (
      !!sessionIndices &&
      sessionIndices.length != courseSection.sessions.length
    ) {
      console.warning(`Provided number of checked conflicts ${sessionIndices.length}
                            does not match number of sessions ${courseSection.sessions.length},
                            ignoring..`);
      sessionIndices = null;
    } else {
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
       */
      const additions = [];

      // Check that there are no session conflicts in course section sessions
      courseSection.sessions.forEach((courseSession, index) => {
        let sessionIndex =
          sessionIndices !== null
            ? sessionIndices[index] // If already checked for conflicts
            : // use provided indices
              this.getAddCourseSessionIndex(courseSession);

        if (sessionIndex === null) {
          // console.error(`Schedule Conflict`);
          return false;
        } else {
          additions.push({
            index: sessionIndex,
            day: courseSession.day_of_week,
            courseSession,
          });
        }
      });

      console.log(`Additions before sort: ${JSON.stringify(additions)}`);
      additions.sort((a1, a2) =>
        a1.day === a2.day
          ? a1.day - a2.day
          : a2.courseSession.time_start - a1.courseSession.time_start
      );
      console.log(`Additions after sort: ${JSON.stringify(additions)}`);
      for (const { index, day, courseSession } of additions) {
        this.dailySessions[day].splice(index, 0, courseSession);

        console.log(
          `Inserted on day ${day} at index ${index} new courseSession ${JSON.stringify(
            courseSession
          )}`
        );
      }

      this.selectedSections.push(courseSection);
      console.log(`Added new courseSection ${JSON.stringify(courseSection)}`);
      return true;
    }
  }

  /**
   * Remove all sessions in courseSection from schedule
   * Does not check if individual course session removal succeeds
   * @param {Course} course
   * @param {CourseSection} courseSection
   */
  removeCourseSection(course, courseSection) {
    if (!courseSection) {
      console.warn(`Ignoring remove null/undefined courseSection`);
      // } else if (courseSection.sessions.length === 0) {
      //   console.error(
      //     `Cannot remove courseSection with no sessions ${JSON.stringify(courseSection)}`
      //   );
    } else {
      for (const courseSession of courseSection.sessions) {
        this._removeCourseSession(courseSession);
      }
      courseSection.selected = false;

      var i;
      for (i = 0; i < this.selectedSections.length; i++) {
        if (this.selectedSections[i].selected == false) {
          this.selectedSections.splice(i, 1);
        }
      }
    }
  }

  /**
   * Removes all sections of course and the course from tracking
   * @param {Course} course
   */
  removeCourse(course) {
    if (!course) {
      console.warn(`Ignoring remove null/undefined course`);
    } else if (course.sections.length === 0) {
      console.error(
        `Cannot remove course with no sections ${JSON.stringify(course)}`
      );
    } else {
      for (const section of course.sections) {
        this.removeCourseSection(course, section);
      }

      var i;
      for (i = 0; i < this.selectedCourses.length; i++) {
        if (this.selectedCourses[i].selected == false) {
          this.selectedCourses.splice(i, 1);
        }
      }
      // console.log(this.selectedCourses.length);
    }
  }

  /**
   * Adds a course selected to internal storage for data retrieval in 'ScheduleEvent'
   * @param {Course} course
   */
  addCourse(course) {
    if (!course) {
      console.warn("Ignoring add null/undefined course");
    } else {
      this.selectedCourses.push(course);
    }
  }
}

export default Schedule;
