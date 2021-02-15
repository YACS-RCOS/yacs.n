/**
 * @module store
 */

import Vue from "vue";
import Vuex from "vuex";
import VueCookies from "vue-cookies";

import {
  getCourses,
  // getDepartments,
  // getSemesters,
  // getSubSemesters,
} from "@/services/YacsService";
import { readableDate, localToUTCDate } from "@/utils";
import { getDefaultSemester } from "@/services/AdminService";
import { client } from "@/plugins/axios";
// import { deepFreeze } from "@/utils";

import { userModule, USER_NAMESPACE } from "./modules/user";
import {
  scheduleModule,
  SCHEDULE_NAMESPACE,
  scheduleTypes,
} from "./modules/schedule";
import { COLOR_NAMESPACE, colorModule } from "./modules/color";

export const TOGGLE_DARK_MODE = "TOGGLE_DARK_MODE";
export const SET_COURSES = "SET_COURSES";
export const SET_SELECTED_SEMESTER = "SET_SELECTED_SEMESTER";
export const SET_SEMESTERS = "SET_SEMESTERS";
export const SET_SUBSEMESTERS = "SET_SUBSEMESTERS";
export const SET_DEPARTMENTS = "SET_DEPARTMENTS";

export const LOAD_COURSES = "LOAD_COURSES";
export const SELECT_SEMESTER = "selectSemester";
export const LOAD_SEMESTERS = "LOAD_SEMESTERS";
export const LOAD_SUBSEMESTERS = "LOAD_SUBSEMESTERS";
export const LOAD_DEPARTMENTS = "LOAD_DEPARTMENTS";

/**
 * @typedef RootState
 * @property {boolean} darkMode
 * @property {Object.<string, number>} coursesById
 * @property {string|null} selectedSemester
 * @property {string[]} semesters
 * @property {import("@/typedef").Subsemester[]} subsemesters
 * @property {import("@/typedef").Department[]} departments
 */

/** @type {RootState} */
const state = {
  darkMode: VueCookies.get("darkMode") === "true",
  coursesById: {},
  selectedSemester: null,
  semesters: [],
  subsemesters: [],
  departments: [],
};

/** @type {import("vuex").StoreOptions<RootState>} */
const storeOptions = {
  state,
  getters: {
    courses: (state) => Object.values(state.coursesById),
    courseById: (state) => (id) => state.coursesById[id],
  },
  mutations: {
    [TOGGLE_DARK_MODE](state) {
      state.darkMode = !state.darkMode;
      Vue.$cookies.set(
        "darkMode",
        state.darkMode,
        null,
        null,
        null,
        null,
        "Strict"
      );
    },
    [SET_COURSES](state, classes) {
      state.coursesById = classes.reduce(
        (coursesById, course) => ({ ...coursesById, [course.id]: course }),
        {}
      );
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
  },
  actions: {
    async [LOAD_COURSES]({ state, commit }) {
      const courses = await getCourses(state.selectedSemester);

      courses.forEach((course) => {
        course.sections.forEach((section) => {
          section.course = course;
          section.sessions.forEach((session) => {
            session.course = course;
            session.courseSection = section;
          });
        });
      });

      commit(SET_COURSES, courses);
      commit(scheduleTypes.mutations.SET_COURSES, courses);
    },
    async [SELECT_SEMESTER]({ state, commit, dispatch }, semester) {
      if (state.selectedSemester === null) {
        semester = await getDefaultSemester();
      }

      if (semester === undefined || semester === state.selectedSemester) {
        return;
      }

      commit(SET_SELECTED_SEMESTER, semester);

      await Promise.all([dispatch(LOAD_COURSES), dispatch(LOAD_SUBSEMESTERS)]);
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
  },
  modules: {
    [USER_NAMESPACE]: userModule,
    [SCHEDULE_NAMESPACE]: scheduleModule,
    [COLOR_NAMESPACE]: colorModule,
  },
};

const store = new Vuex.Store(storeOptions);

export default store;
