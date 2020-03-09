/**
 * @typedef {Object<string, any>} CourseSession
 * @property {string} crn
 * @property {number} day_of_week
 * @property {string} section
 * @property {string} semester
 * @property {string} time_end
 * @property {string} time_start
 */
/**
 * @typedef {Object<string, any>} CourseSection
 * @property {string} crn
 * @property {string} department
 * @property {number} level
 * @property {string} semester
 * @property {CourseSession[]} sessions
 */
/**
 * @typedef {Object<string, any>} Course
 * @property {string} department
 * @property {number} level
 * @property {CourseSection[]} sections
 * @property {string} title
 * @property {Date} date_start
 * @property {Date} date_end
 */

/**
 *
 */
export default class Schedule {
    static SCHEDULE_DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr'];
    // hours indicate start (inclusive) of one hour block with exclusive end e.g. [8, 9) in ascending order
    static SCHEDULE_HOURS = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
    static SCHEDULE_DAY_DURATION = Schedule.SCHEDULE_HOURS[Schedule.SCHEDULE_HOURS.length - 1] - Schedule.SCHEDULE_HOURS[0];

    /** @type {Map<String, Course>} */
    // courses;
    /** @type {Array<CourseSession[]>} */
    dailySessions;

    constructor() {
        this.dailySessions = [];

        for (let d = 0; d < Schedule.SCHEDULE_DAYS.length; d++) {
            this.dailySessions.push([]);
        }
    }

    /**
    * Returns the unique identifier for a course. Modeled after the primary key in the database for
    * a course.
    * @param {CourseSection|CourseSession} courseObj an object that is a subclass of course
    * @returns {string} the unique identifier of a course
    */
    // _getCourseIdentifier(courseObj) {
    //     return courseObj.crn + courseObj.semster;
    // }

    /**
     * Returns the index that newCourseSession should be inserted at or `null` if there
     * is a schedule conflict
     * Assumes that `newCourseSession.time_start != newCourseSession.time_end`
     * @param {CourseSession} newCourseSession
     * @returns {number|null} the index to insert the new course session
     */
    _getAddCourseSessionIndex(newCourseSession) {
        if (!newCourseSession) {
            console.warn(`Ignoring add null/undefined courseSession`);
        } else if (newCourseSession.day_of_week === undefined
            || newCourseSession.time_end === undefined
            || newCourseSession.time_start === undefined) {
            console.error(`Cannot add courseSession with undefined values ${JSON.stringify(newCourseSession)}`);
        } else {
            const daySessions = this.dailySessions[newCourseSession.day_of_week];
            const numSessions = daySessions.length;

            // If daySessions is empty, no conflicts
            if (numSessions === 0) return 0;

            // If session is after latest session, return last index
            if (newCourseSession.time_start >= daySessions[numSessions - 1].time_end
                && newCourseSession.time_end > daySessions[numSessions - 1].time_end) {
                return numSessions;
            }

            // Check courseSessions in the same day as newCourseSession for conflicts
            for (let i = 0; i < daySessions.length; i++) {
                let sess = daySessions[i];

                // If newCourseSession time block is before sess time block return current index
                if (newCourseSession.time_end <= sess.time_start
                    && newCourseSession.time_start < sess.time_start) {
                    return i;

                    // If newCourseSession time block is after sess time block
                } else if (newCourseSession.time_start >= sess.time_end
                    && newCourseSession.time_end > sess.time_end) {
                    // Check next courseSession
                    continue;

                    // Otherwise there is a schedule conflict
                } else {
                    console.error(`Schedule conflict between ${JSON.stringify(newCourseSession)} and ${JSON.stringify(sess)}`);
                    throw {
                        type: 'Schedule Conflict',
                        existingSession: sess,
                        addingSession: newCourseSession,
                    };
                    // return null;
                }
            }

            // Should be unreachable
            return undefined;
        }
    }

    /**
     *
     * @param {CourseSession} courseSession
     * @returns {boolean} if course session was removed from schedule
     */
    _removeCourseSession(courseSession) {
        if (!courseSession) {
            console.warn(`Ignoring remove null/undefined courseSession`);
        } else {
            let i = 0;
            for (const sess of this.dailySessions[courseSession.day_of_week]) {
                if (sess.section === courseSession.section && sess.time_start === courseSession.time_start && sess.time_end === courseSession.time_end && sess.day_of_week === courseSession.day_of_week) {
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
     *
     * @param {CourseSection} courseSection
     * @returns {boolean} if course section was added to schedule
     */
    addCourseSection(course, courseSection) {
        if (!courseSection) {
            console.warn(`Ignoring add null/undefined courseSection`);
        } else if (courseSection.sessions.length === 0) {
            console.error(`Cannot add courseSection with no sessions ${JSON.stringify(courseSection)}`);
        } else {
            /**
             * @type {{index: number, day: number, courseSession: CourseSession}[]}
             * Keeps track of the courseSessions that will be added
             */
            const additions = [];

            // Check that there are no session conflicts in course section sessions
            for (const courseSession of courseSection.sessions) {
                let sessionIndex = this._getAddCourseSessionIndex(courseSession);

                if (sessionIndex === null) {
                    console.error(`Failed to add course section`);
                    return false;
                } else {
                    additions.push({
                        index: sessionIndex,
                        day: courseSession.day_of_week,
                        courseSession
                    });
                }
            }

            console.log(`Additions before sort: ${JSON.stringify(additions)}`);
            additions.sort((a1, a2) => a1.day === a2.day ? a1.day - a2.day : a2.courseSession.time_start - a1.courseSession.time_start);
            console.log(`Additions after sort: ${JSON.stringify(additions)}`);
            for (const { index, day, courseSession } of additions) {
                this.dailySessions[day].splice(index, 0, courseSession);
                // Allow for sessions to have a reference to their parent course
                // but don't copy the sections so we avoid circular JSON (which will cause JSON.stringify to fail).
                // Am giving a 'backpointer' so the ICS schedule can be easily built based on what sessions are
                // currently selected / inserted.
                // eslint-disable-next-line
                let courseInfo = (({sections, ...o}) => o)(course);
                courseSession.course = courseInfo;
                console.log(`Inserted on day ${day} at index ${index} new courseSession ${JSON.stringify(courseSession)}`)
            }

            console.warn("Setting course section to selected=true");
            courseSection.selected = true;

            console.log(`Added new courseSection ${JSON.stringify(courseSection)}`);
            return true;
        }
    }

    /**
     * Remove all sessions in courseSection from schedule
     * Does not check if individual course session removal succeeds
     * @param {CourseSection} courseSection
     */
    removeCourseSection(courseSection) {
        if (!courseSection) {
            console.warn(`Ignoring remove null/undefined courseSection`);
        } else if (courseSection.sessions.length === 0) {
            console.error(`Cannot remove courseSection with no sessions ${JSON.stringify(courseSection)}`);
        } else {
            for (const courseSession of courseSection.sessions) {
                this._removeCourseSession(courseSession);
            }
            courseSection.selected = false;
        }
    }

    /**
     * Adds course to the list of added courses
     * @param {Course} course
     * @returns {boolean} if course was added
     */
    addCourse(course) {
        console.log(`Adding new course ${JSON.stringify(course)}`)
        if (!course) {
            console.warn(`Ignoring add null/undefined course`);
        } else if (course.sections.length === 0) {
            console.error(`Cannot add course with no sections ${JSON.stringify(course)}`);
        } else {
            if (!(this._getCourseIdentifier(course) in this.courses)) {
                this.courses[this._getCourseIdentifier(course)] = course;
                return true;
            }
        }
        return false;
    }

    /**
     * Removes all sections of course
     * @param {Course} course
     */
    removeCourse(course) {
        if (!course) {
            console.warn(`Ignoring remove null/undefined course`);
        } else if (course.sections.length === 0) {
            console.error(`Cannot remove course with no sections ${JSON.stringify(course)}`);
        } else {
            for (const section of course.sections) {
                this.removeCourseSection(section);
            }
            // this.removeCourseSection(course.sections[sectionIndex]);
            //   this.courses.splice(this.courses.indexOf(course), 1);
        }
    }

    getCourseBySubclass(courseSession) {
        return this.courses[this._getCourseIdentifier(courseSession)];
    }
}