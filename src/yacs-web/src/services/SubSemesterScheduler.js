import {
    ScheduleService as Schedule,
} from '@/services';

export default class SubSemesterScheduler {
    schedules;
    scheduleSubsemesters;

    constructor () {
        this.schedules = [];
        this.scheduleSubsemesters = [];
    }

    addSubSemester (subsemester) {
        this.schedules.push(new Schedule());
        this.scheduleSubsemesters.push(subsemester);
    }

    /**
     * 
     * @param {Course} course 
     * @param {Subsemester} subsemester
     */
    withinCourseDuration(course, subsemester) {
        return (course.date_start.getTime() == subsemester.date_start.getTime() &&
            course.date_end.getTime() >= subsemester.date_end.getTime()) ||
            (course.date_end.getTime() == subsemester.date_end.getTime() &&
            course.date_start.getTime() <= subsemester.date_start.getTime());
    }

    addCourseSection (course, section) {
        const scheduleSessionIndices = {};
        for (const [index, schedule] of this.schedules.entries()) {
            if (this.withinCourseDuration(course, this.scheduleSubsemesters[index])) {
                try {
                    const sessionIndices = [];
                    for (const session of section.sessions) {
                        sessionIndices.push(schedule.getAddCourseSessionIndex(session));
                    }
                    scheduleSessionIndices[index] = sessionIndices;
                } catch (err) {
                    if (err.type === 'Schedule Conflict') {
                        err.subsemester = this.scheduleSubsemesters[index];
                        console.log(err);
                        throw err;
                    }
                }
            }
        }

        Object.entries(scheduleSessionIndices).forEach(([scheduleIndex, sessionIndices]) => {
            this.schedules[scheduleIndex].addCourseSection(course, section, sessionIndices);
        })
    }

    removeCourseSection (section) {
        this.schedules.forEach(s => s.removeCourseSection(section));
    }

    removeAllCourseSections (course) {
        this.schedules.forEach(s => s.removeCourse(course));
    }
}