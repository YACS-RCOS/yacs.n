/** @module store/schedule */

// import CourseScheduler from "@/controllers/CourseScheduler";

import { colorTypes } from "@/store/modules/color";

import { prefixNamespacedTypes } from "@/utils";

const {
  namespace: SCHEDULE_NAMESPACE,
  local: types,
  ...scheduleTypes
} = prefixNamespacedTypes("schedule", {
  getters: {},
  mutations: {
    SET_COURSES: "SET_COURSES",
    SELECT_COURSE: "SELECT_COURSE",
    UNSELECT_COURSE: "UNSELECT_COURSE",
    SELECT_COURSE_SECTION: "SELECT_COURSE_SECTION",
    UNSELECT_COURSE_SECTION: "UNSELECT_COURSE_SECTION",
  },
  actions: {
    SELECT_COURSE: "SELECT_COURSE",
    UNSELECT_COURSE: "UNSELECT_COURSE",
    SELECT_COURSE_SECTION: "SELECT_COURSE_SECTION",
    UNSELECT_COURSE_SECTION: "UNSELECT_COURSE_SECTION",
  },
});

/**
 * @typedef {import("../index").RootState} RootState
 * @typedef ScheduleModuleState
 * @property {string[]} selectedCourseIds
 * @property {Object.<string, import("@/typedef").Course>} selectedCoursesById
 * @property {string[]} selectedCourseSectionCrns
 * @property {Object.<string, import("@/typedef").CourseSection>} selectedCourseSectionsByCrn
 */

/** @type {ScheduleModuleState} */
const state = {
  // scheduler: new CourseScheduler(),
  selectedCourseIds: [],
  selectedCoursesById: {},
  selectedCourseSectionCrns: [],
  selectedCourseSectionsByCrn: {},
};

/** @type {import("vuex").GetterTree<ScheduleModuleState, RootState>} */
const getters = {
  selectedCourses: (state, getters, rootState, rootGetters) =>
    state.selectedCourseIds.map((courseId) => rootGetters.courseById(courseId)),
  selectedCourseSections: (state, getters) => {
    const selectedCourseSectionCrns = new Set(state.selectedCourseSectionCrns);
    return getters.selectedCourses
      .map((course) => course.sections)
      .flat()
      .filter((section) => selectedCourseSectionCrns.has(section.crn));
  },
};

/** @type {import("vuex").MutationTree<ScheduleModuleState>} */
const mutations = {
  async [types.mutations.SET_COURSES](state, courses) {
    const selectedCoursesById = {};
    const selectedCourseSectionsByCrn = {};
    const selectedCourseIds = [];
    const selectedCourseSectionCrns = [];
    courses.forEach((course) => {
      selectedCoursesById[course.id] =
        state.selectedCoursesById[course.id] || false;

      if (selectedCoursesById[course.id]) {
        selectedCourseIds.push(course.id);
      }

      course.sections.forEach((section) => {
        selectedCourseSectionsByCrn[section.crn] =
          state.selectedCourseSectionsByCrn[section.crn] || false;

        if (selectedCourseSectionsByCrn[section.crn]) {
          selectedCourseSectionCrns.push(section.crn);
        }
      });
    });

    state.selectedCourseIds = selectedCourseIds;
    state.selectedCourseSectionCrns = selectedCourseSectionCrns;
    state.selectedCoursesById = selectedCoursesById;
    state.selectedCourseSectionsByCrn = selectedCourseSectionsByCrn;
  },
  async [types.mutations.SELECT_COURSE](state, courseId) {
    state.selectedCourseIds.push(courseId);
    state.selectedCoursesById[courseId] = true;
  },
  async [types.mutations.SELECT_COURSE_SECTION](state, courseSectionCrn) {
    state.selectedCourseSectionCrns.push(courseSectionCrn);
    state.selectedCourseSectionsByCrn[courseSectionCrn] = true;
  },
  async [types.mutations.UNSELECT_COURSE](state, courseId) {
    state.selectedCourseIds.splice(
      state.selectedCourseIds.findIndex((id) => id === courseId),
      1
    );
    state.selectedCoursesById[courseId] = false;
  },
  async [types.mutations.UNSELECT_COURSE_SECTION](state, courseSectionCrn) {
    state.selectedCourseSectionCrns.splice(
      state.selectedCourseSectionCrns.findIndex(
        (crn) => crn === courseSectionCrn
      ),
      1
    );
    state.selectedCourseSectionsByCrn[courseSectionCrn] = false;
  },
};

/** @type {import("vuex").ActionTree<ScheduleModuleState, RootState>} */
const actions = {
  async [types.actions.SELECT_COURSE](
    { state, commit, dispatch },
    /** @type {{courseId: string}} */
    { courseId }
  ) {
    if (state.selectedCoursesById[courseId]) {
      return;
    }

    dispatch(colorTypes.actions.ASSIGN_COLOR, courseId, { root: true });

    commit(types.mutations.SELECT_COURSE, courseId);

    // state.scheduler.addCourse(rootGetters.courseById(courseId));
  },
  async [types.actions.SELECT_COURSE_SECTION](
    { state, commit, dispatch },
    /** @type {{courseId: string, courseSectionCrn: string}} */
    { courseId, courseSectionCrn }
  ) {
    if (state.selectedCourseSectionsByCrn[courseSectionCrn]) {
      return;
    }

    if (!state.selectedCoursesById[courseId]) {
      dispatch(types.actions.SELECT_COURSE, { courseId });
    }

    commit(types.mutations.SELECT_COURSE_SECTION, courseSectionCrn);

    // /** @type {import("@/typedef").Course} */
    // const course = rootGetters.courseById(courseId);

    // const courseSection = course.sections.find(
    //   (section) => section.crn === courseSectionCrn
    // );

    // state.scheduler.addCourseSection(course, courseSection);
  },
  async [types.actions.UNSELECT_COURSE](
    { state, commit, dispatch, rootGetters },
    /** @type {{courseId: string}} */
    { courseId }
  ) {
    if (!state.selectedCoursesById[courseId]) {
      return;
    }

    const course = rootGetters.courseById(courseId);

    for (const section of course.sections) {
      if (state.selectedCourseSectionsByCrn[section.crn]) {
        dispatch(types.actions.UNSELECT_COURSE_SECTION, {
          courseSectionCrn: section.crn,
        });
      }
    }

    dispatch(colorTypes.actions.RELEASE_COLOR, courseId, { root: true });

    commit(types.mutations.UNSELECT_COURSE, courseId);

    // state.scheduler.removeAllCourseSections(rootGetters.courseById(courseId));
  },
  async [types.actions.UNSELECT_COURSE_SECTION](
    { state, commit },
    /** @type {{courseId: string, courseSectionCrn: string}} */
    { courseSectionCrn }
  ) {
    if (!state.selectedCourseSectionsByCrn[courseSectionCrn]) {
      return;
    }

    commit(types.mutations.UNSELECT_COURSE_SECTION, courseSectionCrn);

    /** @type {import("@/typedef").Course} */
    // const course = rootGetters.courseById(courseId);

    // const courseSection = course.sections.find(
    // (section) => section.crn === courseSectionCrn
    // );

    // state.scheduler.removeCourseSection(course, courseSection);
  },
};

/** @type {import("vuex").Module<ScheduleModuleState, RootState>} */
const scheduleModule = {
  state,
  getters,
  mutations,
  actions,
  namespaced: true,
};

export { scheduleModule, scheduleTypes, SCHEDULE_NAMESPACE };
