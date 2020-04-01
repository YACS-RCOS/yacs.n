import Vue from 'vue';

import store from './index';

import Schedule from '@/controllers/Schedule';

export const INIT_COURSES = 'INIT_COURSES';
export const INIT_SELECTED_COURSES = 'INIT_SELECTED_COURSES';

export const SELECT_COURSE = 'SELECT_COURSE';
export const UNSELECT_COURSE = 'UNSELECT_COURSE';
export const SELECT_COURSE_SECTION = 'SELECT_COURSE_SECTION';
export const UNSELECT_COURSE_SECTION = 'UNSELECT_COURSE_SECTION';

export const ADD_SCHEDULE = 'ADD_SCHEDULE';
export const REMOVE_SCHEDULE = 'REMOVE_SCHEDULE';

export const ADD_COURSE_SECTION = 'ADD_COURSE_SECTION';
export const REMOVE_COURSE_SECTION = 'REMOVE_COURSE_SECTION';

export const NEXT_SCHEDULE_INDEX = 'NEXT_SCHEDULE_INDEX';

export default {
  [INIT_COURSES](state, { courses, sections, sessions }) {
    state._courses = Object.assign({}, state._courses, courses);
    state._courseSections = Object.assign({}, state._courseSections, sections);
    state._courseSessions = Object.assign({}, state._courseSessions, sessions);
  },
  [INIT_SELECTED_COURSES](state) {
    state.selectedCourseIds.splice(0, state.selectedCourseIds.length);
    state.selectedCourseSectionIds.splice(0, state.selectedCourseSectionIds.length);
  },
  [SELECT_COURSE](state, { id }) {
    state._courses[id].selected = true;
    state.selectedCourseIds.push(id);
  },
  [UNSELECT_COURSE](state, { id }) {
    store.commit(UNSELECT_COURSE_SECTION, {
      ids: store.getters
        .getSections(state._courses[id].sectionIds)
        .filter(s => s.selected)
        .map(s => s.id)
    });
    state._courses[id].selected = false;
    state.selectedCourseIds.splice(state.selectedCourseIds.indexOf(id), 1);
  },
  [SELECT_COURSE_SECTION](state, { id }) {
    state._courseSections[id].selected = true;
    state.selectedCourseSectionIds.push(id);
  },
  [UNSELECT_COURSE_SECTION](state, { id, ids }) {
    if (id) {
      ids = [id];
    }
    for (let id of ids) {
      state._courseSections[id].selected = false;
      state.selectedCourseSectionIds.splice(state.selectedCourseSectionIds.indexOf(id), 1);
    }
  },
  [ADD_SCHEDULE](state, { id, schedule = new Schedule() }) {
    if (
      !state.rootScheduleId ||
      (schedule.scheduleIds && schedule.scheduleIds.includes(state.rootScheduleId))
    ) {
      state.rootScheduleId = id;
    }
    Vue.set(state._schedules, id, schedule);
  },
  [REMOVE_SCHEDULE](state, { id }) {
    if (id == state.rootScheduleId) {
      state.rootScheduleId = null;
    }
    Vue.delete(state._schedules, id);
  },
  [ADD_COURSE_SECTION](state, { scheduleId, sectionId, sessionIndices }) {
    // state._schedules[scheduleId ?? state.rootScheduleId]._addCourseSection(
    store.getters
      .getSchedule(scheduleId ?? state.rootScheduleId)
      ._addCourseSection(store.getters.getSection(sectionId), sessionIndices);
  },
  [REMOVE_COURSE_SECTION](state, { scheduleId, sectionId, courseId }) {
    const schedule = state._schedules[scheduleId ?? state.rootScheduleId];
    if (courseId) {
      schedule._removeAllCourseSections(store.getters.getCourse(courseId));
    } else {
      schedule._removeCourseSection(store.getters.getSection(sectionId));
    }
  },
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
