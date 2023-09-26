import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

import { getDefaultSemester } from "@/services/AdminService";
import { getCourses } from "@/services/YacsService";
import { readableDate, localToUTCDate } from "@/utils";

import { userModule, USER_NAMESPACE } from "./modules/user";

const client = axios.create({
  baseURL: "/api",
});

Vue.use(Vuex);

// Constants are UPPER_SNAKE_CASE but we set the values to
//  camelCase so when using mapMutations, mapActions, etc.
//  they will map to camelCase names
export const COURSES = "courses";
export const GET_COURSE_BY_ID = "getCourseById";

export const COOKIE_DARK_MODE = "darkMode";
export const TOGGLE_DARK_MODE = "toggleDarkMode";
export const SAVE_DARK_MODE = "saveDarkMode";
export const RESET_DARK_MODE = "resetDarkMode";
export const TOGGLE_COLOR_BLIND_ASSIST = "toggleColorBlindAssist";
export const SET_COURSES = "setCourses";
const SET_IS_LOADING_COURSES = "SET_IS_LOADING_COURSES";
export const SET_SELECTED_SEMESTER = "setSelectedSemester";
export const SET_SEMESTERS = "setSemesters";
export const SET_SUBSEMESTERS = "setSubsemesters";
export const SET_DEPARTMENTS = "setDepartments";

export const LOAD_COURSES = "loadCourses";
export const SELECT_SEMESTER = "selectSemester";
export const LOAD_SEMESTERS = "loadSemesters";
export const LOAD_SUBSEMESTERS = "loadSubsemesters";
export const LOAD_DEPARTMENTS = "loadDepartments";

const store = new Vuex.Store({
  state: {
    darkMode: false,
    colorBlindAssist: false,
    coursesById: {},
    isLoadingCourses: false,
    selectedSemester: null,
    semesters: [],
    subsemesters: [],
    departments: [],
    selectedCourses: {},
  },
  getters: {
    [COURSES]: (state) => Object.values(state.coursesById),
    [GET_COURSE_BY_ID]: (state) => (id) => state.coursesById[id],
    darkModeState: (state) => {
      return state.darkMode;
    },
    colorBlindAssistState: (state) => {
      return state.colorBlindAssist;
    },
    selectedCourses: state => state.selectedCourses,
  },
  mutations: {
    [TOGGLE_DARK_MODE](state, isDarkMode = null) {
      state.darkMode = isDarkMode === null ? !state.darkMode : isDarkMode;

      const bodyClassList = document.getElementsByTagName("body")[0].classList;
      if (state.darkMode) {
        bodyClassList.add("dark");
      } else {
        bodyClassList.remove("dark");
      }
    },
    [SAVE_DARK_MODE](state) {
      Vue.$cookies.set(
        COOKIE_DARK_MODE,
        state.darkMode,
        null,
        null,
        null,
        null,
        "Strict"
      );
    },
    [RESET_DARK_MODE](state) {
      Vue.$cookies.remove(COOKIE_DARK_MODE);
      state.darkMode = !window.matchMedia("(prefers-color-scheme: dark)")
        .matches;
    },
    [TOGGLE_COLOR_BLIND_ASSIST](state, isCBAssist = null) {
      state.colorBlindAssist =
        isCBAssist === null ? !state.colorBlindAssist : isCBAssist;

      Vue.$cookies.set(
        "colorBlindAssist",
        state.colorBlindAssist,
        null,
        null,
        null,
        null,
        "Strict"
      );
    },
    [SET_COURSES](state, classes) {
      state.coursesById = classes.reduce((coursesById, course) => {
        coursesById[course.id] = course;
        return coursesById;
      }, {});
    },
    [SET_IS_LOADING_COURSES](state, isLoadingCourses) {
      state.isLoadingCourses = isLoadingCourses;
    },
    [SET_SELECTED_SEMESTER](state, semester) {
      state.selectedSemester = semester;
    },
    [SET_SUBSEMESTERS](state, subsemesters) {
      state.subsemesters = subsemesters;
    },
    [SET_DEPARTMENTS](state, departments) {
      state.departments = departments;
    },
    [SET_SEMESTERS](state, semesters) {
      state.semesters = semesters;
    },
    ADD_COURSE(state, course) {
      Vue.set(state.selectedCourses, course.id, course);
    },
    REMOVE_COURSE(state, course) {
      Vue.delete(state.selectedCourses, course.id, course);
    },
  },
  actions: {
    async [LOAD_COURSES]({ state, commit }) {
      commit(SET_IS_LOADING_COURSES, true);

      const courses = await getCourses(state.selectedSemester);

      commit(SET_COURSES, courses);
      commit(SET_IS_LOADING_COURSES, false);
    },
    async [SELECT_SEMESTER]({ state, commit, dispatch }, semester) {
      if (state.semesters.length === 0) {
        await dispatch(LOAD_SEMESTERS);
      }

      if (!semester && Vue.$cookies.get("selectedSemester")) {
        semester = Vue.$cookies.get("selectedSemester");
      }

      if (!semester || !state.semesters.find((s) => s.semester === semester)) {
        semester = await getDefaultSemester();
      }

      if (!semester || semester === state.selectedSemester) {
        return;
      }

      commit(SET_SELECTED_SEMESTER, semester);
      Vue.$cookies.set(
        "selectedSemester",
        semester,
        null,
        null,
        null,
        null,
        "Strict"
      );

      await dispatch(LOAD_SUBSEMESTERS);

      // Do not wait for load courses to complete
      // This is a slow operation and we have another
      //  state property `isLoadingCourses` that is
      //  meant to track the progress of this operation
      dispatch(LOAD_COURSES);
    },
    async [LOAD_SEMESTERS]({ commit }) {
      const semesters = await client.get("/semester").then((res) => res.data);

      commit(SET_SEMESTERS, semesters);
    },
    async [LOAD_SUBSEMESTERS]({ state, commit }) {
      const subsemesters = await client
        .get("/subsemester", {
          params: {
            semester: state.selectedSemester,
          },
        })
        .then(({ data }) => {
          return data.map((subsemester) => {
            subsemester.date_start = localToUTCDate(
              new Date(subsemester.date_start)
            );
            subsemester.date_end = localToUTCDate(
              new Date(subsemester.date_end)
            );
            subsemester.date_start_display = readableDate(
              subsemester.date_start
            );
            subsemester.date_end_display = readableDate(subsemester.date_end);
            // Used to determine what semester the subsemester is part of
            subsemester.semester_name = subsemester.parent_semester_name;
            subsemester.display_string = subsemester.semester_part_name
              ? subsemester.semester_part_name
              : `${subsemester.date_start_display} - ${subsemester.date_end_display}`;

            return subsemester;
          });
        });

      commit(SET_SUBSEMESTERS, subsemesters);
    },
    async [LOAD_DEPARTMENTS]({ commit }) {
      const departments = await client.get("/department").then(({ data }) => {
        return data;
      });

      commit(SET_DEPARTMENTS, departments);
    },
    addCourse({commit},course){
      commit('ADD_COURSE',course);
    },
    removeCourse({commit, course}){
      commit('REMOVE_COURSE',course);
    },
  },
  modules: {
    [USER_NAMESPACE]: userModule,
  },
});

export default store;
