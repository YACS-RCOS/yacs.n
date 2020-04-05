import Vue from 'vue';

import store from './index';

import Schedule from '@/controllers/Schedule';

// Mutations for initializing state
export const INIT_COURSES = 'INIT_COURSES';
export const INIT_SELECTED_COURSES = 'INIT_SELECTED_COURSES';
export const INIT_SCHEDULES = 'INIT_SCHEDULES';

// User initiated mutations
export const SELECT_COURSE = 'SELECT_COURSE';
export const UNSELECT_COURSE = 'UNSELECT_COURSE';
export const SELECT_COURSE_SECTION = 'SELECT_COURSE_SECTION';
export const UNSELECT_COURSE_SECTION = 'UNSELECT_COURSE_SECTION';

// Schedule/system mutations
export const ADD_SCHEDULE = 'ADD_SCHEDULE';
export const REMOVE_SCHEDULE = 'REMOVE_SCHEDULE';

// This is different from selecting course/sections
// Selecting means the user has clicked on a course/section
// Adding is when a section is added to a schedule controller
export const ADD_COURSE_SECTION = 'ADD_COURSE_SECTION';
export const REMOVE_COURSE_SECTION = 'REMOVE_COURSE_SECTION';

export const NEXT_SCHEDULE_INDEX = 'NEXT_SCHEDULE_INDEX';

export default {
  [INIT_COURSES](state, { courses, sections, sessions }) {
    state._courses = Object.assign({}, state._courses, courses);
    state._courseSections = Object.assign({}, state._courseSections, sections);
    state._courseSessions = Object.assign({}, state._courseSessions, sessions);
  },
  // Perhaps a misnomer but more so used to reset selected courses
  // during hot reloads
  [INIT_SELECTED_COURSES](state) {
    state.selectedCourseIds.splice(0, state.selectedCourseIds.length);
    state.selectedCourseSectionIds.splice(0, state.selectedCourseSectionIds.length);
  },
  [INIT_SCHEDULES](state) {
    state._schedules = {}; // Not reactive but old objects should get garbage collected?
    state.scheduleIdIndex = 0;
    state.rootScheduleId = null;
  },
  [SELECT_COURSE](state, { courseId }) {
    // Maybe dangerous to have two sources of truth for selected state
    //  but having selected on the actual course object is just too
    //  convenient to not have imo. As long as changes to selected state
    //  are done solely through the following mutations, they should be
    //  always in sync
    state._courses[courseId].selected = true;
    state.selectedCourseIds.push(courseId);
  },
  // Unselect course and all its sections
  [UNSELECT_COURSE](state, { courseId }) {
    // This is kind of a hack and perhaps could be avoided by delegating
    // to an action
    state._courses[courseId].sectionIds
      .filter(sectionId => state._courseSections[sectionId].selected)
      .forEach(sectionId => store.commit(UNSELECT_COURSE_SECTION, { sectionId }));

    state._courses[courseId].selected = false;
    state.selectedCourseIds.splice(state.selectedCourseIds.indexOf(courseId), 1);
  },
  [SELECT_COURSE_SECTION](state, { sectionId }) {
    state._courseSections[sectionId].selected = true;
    state.selectedCourseSectionIds.push(sectionId);
  },
  [UNSELECT_COURSE_SECTION](state, { sectionId }) {
    state._courseSections[sectionId].selected = false;
    state.selectedCourseSectionIds.splice(state.selectedCourseSectionIds.indexOf(sectionId), 1);
  },
  // Add a new schedule to the schedule tree with the given id
  // By default adds a Schedule instance
  [ADD_SCHEDULE](state, { id, schedule = new Schedule() }) {
    if (
      !state.rootScheduleId ||
      (schedule.scheduleIds && schedule.scheduleIds.includes(state.rootScheduleId))
    ) {
      // If there is no root node or the provided schedule contains
      // the current root node as child schedule, set provided
      // schedule as root node
      state.rootScheduleId = id;
    }
    Vue.set(state._schedules, id, schedule);
  },
  // This functionality is not fully realized as of now since it is not
  //  actually being used. When a future schedule type actually involves
  //  creating/removing child schedules, this implementation will be
  //  better fleshed out
  // But the general idea is that removing a schedule will remove all
  //  children schedules. If the schedule is the root node, the entire
  //  tree is removed.
  // An additional consideration is if a schedule requires an exact number
  //  of children schedules. If a child schedule is to be removed from that
  //  type of schedule, it would require the parent also to be removed.
  //  e.g.  There are three subsemesters so SubSemesterSchedule must have
  //        three children schedules. If a child schedule is to be removed,
  //        that should mean the SubSemesterSchedule should also be removed.
  [REMOVE_SCHEDULE](state, { id }) {
    if (id == state.rootScheduleId) {
      state.rootScheduleId = null;
    }
    Vue.delete(state._schedules, id);
  },
  // Calls the _addCourseSection method of the given scheduleId
  // If none is provided, defaults to the root schedule.
  // The default should be the main use case.
  [ADD_COURSE_SECTION](state, { scheduleId, sectionId, sessionIndices }) {
    state._schedules[scheduleId ?? state.rootScheduleId]._addCourseSection(
      state._courseSections[sectionId],
      sessionIndices
    );
  },
  // Calls the _removeCourseSection or _removeAllCourseSection depending
  //  on whether sectionId or courseId is provided respectively.
  [REMOVE_COURSE_SECTION](state, { scheduleId, sectionId, courseId }) {
    const schedule = state._schedules[scheduleId ?? state.rootScheduleId];
    if (courseId) {
      schedule._removeAllCourseSections(courseId);
    } else {
      schedule._removeCourseSection(sectionId);
    }
  },
  // Used by the system to generate schedule IDs
  // Seems crude but works
  [NEXT_SCHEDULE_INDEX](state) {
    state.scheduleIdIndex++;
    while (state._schedules[state.scheduleIdIndex]) {
      if (state.scheduleIdIndex > 100000) {
        state.scheduleIdIndex = 0;
      }

      state.scheduleIdIndex++;
    }
  }
};
