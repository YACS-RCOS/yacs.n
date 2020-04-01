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
    _schedules: {},
    scheduleIdIndex: 0,
    rootScheduleId: null
  },
  mutations,
  actions,
  getters: {
    courses: state => Object.values(state._courses),
    getCourse: state => id => state._courses[id],
    getCourses: (_, getters) => ids => ids.map(id => getters.getCourse(id)),
    sections: state => Object.values(state._courseSections),
    getSection: state => id => state._courseSections[id],
    getSections: (_, getters) => ids => ids.map(id => getters.getSection(id)),
    sessions: state => Object.values(state._courseSessions),
    getSession: state => id => state._courseSessions[id],
    getSessions: (_, getters) => ids => ids.map(id => getters.getSession(id)),
    selectedCourses: (state, getters) => getters.getCourses(state.selectedCourseIds),
    selectedCourseSections: (state, getters) => getters.getSections(state.selectedCourseSectionIds),
    schedules: state => Object.values(state._schedules),
    getSchedule: state => id => state._schedules[id ?? state.rootScheduleId]
  },
  modules: {}
});
