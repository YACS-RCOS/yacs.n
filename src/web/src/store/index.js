import '@/typedef';

import Vue from 'vue';
import Vuex from 'vuex';

import mutations from './mutations';
import actions from './actions';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    _courses: {},
    _courseSections: {},
    _courseSessions: {},
    selectedCourseIds: [],
    selectedCourseSectionIds: [],
    // In depth explanation about schedules, how they are stored,
    // what errors they throw, how they work, etc. attached
    // at very bottom
    _schedules: {},
    // Used to generate schedule IDs
    scheduleIdIndex: 0,
    // The root schedule in the aforementioned "Schedule tree"
    // There MUST be a path from the root schedule to every schedule
    //  in the tree.
    rootScheduleId: null
  },
  mutations,
  actions,
  getters: {
    courses: state => Object.values(state._courses),
    getCourse: state => id => state._courses[id],
    getCourses: (_, getters) => ids => ids.map(id => getters.getCourse(id)),
    sections: state => Object.values(state._courseSections),
    getCourseSection: state => id => state._courseSections[id],
    getCourseSections: (_, getters) => ids => ids.map(id => getters.getCourseSection(id)),
    sessions: state => Object.values(state._courseSessions),
    getCourseSession: state => id => state._courseSessions[id],
    getCourseSessions: (_, getters) => ids => ids.map(id => getters.getCourseSession(id)),
    selectedCourses: (state, getters) => getters.getCourses(state.selectedCourseIds),
    selectedCourseSections: (state, getters) =>
      getters.getCourseSections(state.selectedCourseSectionIds),
    schedules: state => Object.values(state._schedules),
    getSchedule: state => id => state._schedules[id ?? state.rootScheduleId]
  },
  modules: {}
});

/*
For schedules, I'm currently thinking about storing them
in a "Schedule tree".

Basically, every schedule MUST expose the following public methods:
- addCourseSection(section: CourseSection)
- removeCourseSection(section: CourseSection)
MAY expose these:
- removeAllCourseSections(course: Course)
- checkScheduleConflict(section: CourseSection) // not yet implemented

Leaf nodes MUST have dailySessions: CourseSession[][]
  which represents the CourseSessions in a weekly schedule and is 
  passed to Schedule.vue

All other nodes MUST have scheduleIds: string[]
  which represents the children Schedules that compose this schedule

The error thrown by all nodes MUST contain the following properties:
{
  existingCourseSession: CourseSession
  newCourseSession: CourseSession
  type: "Schedule Conflict"
}
However they are free to add properties to the error object as needed. 

CourseSections are added/removed from the root node and then propagated
down to the leaf nodes. Schedule conflicts are generated at the leaf nodes
and propagated up to the root node. 

This allows composition of schedules, with each layer of the 
composition handling a different aspect of scheduling. Additionally, 
hopefully this approach is extensible so new scheduling options can 
be easily introduced without drastic redesign. 

For example, the basic structure that is in play at the moment 
involves two types of schedules:
  1) Schedule.js - Represents weekly schedule
  2) SubSemesterSchedule.js - Represents schedule spanning multiple
                                subsemesters
Their relationship is: SubSemesterSchedule has many Schedule 
                          (one for each subsemester)

Since Schedule has no concept of SubSemesters, we delegate that
responsibility to SubSemesterSchedule. SubsemesterSchedule internally
maps a subsemester to a Schedule. Thus, when we add a CourseSection,
SubSemesterSchedule will check which subsemester(s) the CourseSection
belongs to and will pass the CourseSection to the appropriate Schedules.

Given two subsemesters A and B:
_schedules = {
  0: Schedule,
  1: Schedule,
  2: SubSemesterSchedule{
    scheduleIds: [0, 1]
  }
}
_rootScheduleId = 2

Hypothetically, if we wanted to say add the concepts of semeseters, we 
could define a SemesterSchedule that would contain a list of scheduleIds. 
The role of SemesterSchedule would be to check which semester a course
belonged to and pass it to the appropriate schedule. So for example, given
Summer semester and Fall semester. Summer has subsemesters I and II while 
Fall has no subsemesters. We could create the following SemesterSchedule:

SemesterSchedule{
  children: {
    Summer: SubsemesterSchedule{
      children: {
        I: Schedule,
        II: Schedule,
      }
    },
    Fall: Schedule
  }
}

Notice how because Fall doesn't have subsemesters, we can use the base
Schedule class. However, for Summer, we create a SubSemesterSchedule 
which then contains two children Schedules, one for each subsemester. 

If the user were to add the following CourseSection:

CourseSection{
  semester: Summer,
  subsemester: II,
}

The call flow would look like:

SemesterSchedule.addCourseSection()
-> Summer:SubsemesterSchedule.addCourseSection()
  -> II:Schedule.addCourseSection()

Similarly, just as schedule changes are propagated down, schedule
conflicts are propagated up. This allows each layer to add their information
to the schedule conflict error object. 

e.g. If the previous example caused a schedule conflict, the error
object content would be transformed as so:

Error thrown by Summer:II:Schedule (lowest level)
{
  existingCourseSession:
  newCourseSession:
}

Error thrown by Summer:SubSemesterSchedule
{
  existingCourseSession:
  newCourseSession:
  subsemester: II
}

Error thrown at the top level
{
  existingCourseSession:
  newCourseSession:
  subsemester: II
  semester: Summer
}
*/
