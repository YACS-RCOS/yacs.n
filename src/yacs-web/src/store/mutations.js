export const INIT_COURSES = 'INIT_COURSES';
export const INIT_SELECTED_COURSES = 'INIT_SELECTED_COURSES';

export const SELECT_COURSE = 'SELECT_COURSE';
export const UNSELECT_COURSE = 'UNSELECT_COURSE';
export const SELECT_COURSE_SECTION = 'SELECT_COURSE_SECTION';
export const UNSELECT_COURSE_SECTION = 'UNSELECT_COURSE_SECTION';

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
    state._courses[id].selected = false;
    state.selectedCourseIds.splice(state.selectedCourseIds.indexOf(id), 1);
  },
  [SELECT_COURSE_SECTION](state, { id }) {
    state._courseSections[id].selected = true;
    state.selectedCourseSectionIds.push(id);
  },
  [UNSELECT_COURSE_SECTION](state, { id }) {
    state._courseSections[id].selected = false;
    state.selectedCourseSectionIds.splice(state.selectedCourseSectionIds.indexOf(id), 1);
  }
};
