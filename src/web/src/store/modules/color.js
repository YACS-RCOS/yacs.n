/** @module store/color */

import Vue from "vue";

import { prefixNamespacedTypes } from "@/utils";

const COLORS = [
  "#ffd4df",
  "#ceeffc",
  "#fff4d0",
  "#dcf7da",
  "#f7e2f7",
  "#ede6df",
  "#ffe9cf",
];
const TEXT_COLORS = [
  "#d1265d",
  "#1577aa",
  "#bf8a2e",
  "#008a2e",
  "#853d80",
  "#9d5733",
  "#d9652b",
];
const BORDER_COLORS = [
  "#ff2066",
  "#00aff2",
  "#ffcb45",
  "#48da58",
  "#d373da",
  "#a48363",
  "#ff9332",
];
const NUM_COLORS = 7;

const {
  namespace: COLOR_NAMESPACE,
  local: types,
  ...colorTypes
} = prefixNamespacedTypes("color", {
  getters: {
    GET_BACKGROUND_COLOR: "getBackgroundColor",
    GET_BORDER_COLOR: "getBorderColor",
    GET_TEXT_COLOR: "getTextColor",
  },
  mutations: {
    ASSIGN_COLOR: "ASSIGN_COLOR",
    RELEASE_COLOR: "RELEASE_COLOR",
  },
  actions: {
    ASSIGN_COLOR: "ASSIGN_COLOR",
    RELEASE_COLOR: "RELEASE_COLOR",
  },
});

/**
 * @typedef {import("../index").RootState} RootState
 * @typedef ColorModuleState
 * @property {{[id: string]: number}} colorAssignments
 * @property {number[]} assignmentCounts
 */

/** @type {ColorModuleState} */
const state = {
  colorAssignments: {},
  assignmentCounts: Array.from({ length: NUM_COLORS }).fill(0),
};

/** @type {import("vuex").GetterTree<ColorModuleState, RootState>} */
const getters = {
  [types.getters.GET_BACKGROUND_COLOR]: (state) => (id) => {
    return COLORS[state.colorAssignments[id]];
  },
  [types.getters.GET_BORDER_COLOR]: (state) => (id) => {
    return BORDER_COLORS[state.colorAssignments[id]];
  },
  [types.getters.GET_TEXT_COLOR]: (state) => (id) => {
    return TEXT_COLORS[state.colorAssignments[id]];
  },
};

/** @type {import("vuex").MutationTree<ColorModuleState>} */
const mutations = {
  [types.mutations.ASSIGN_COLOR](state, { id, assignment }) {
    Vue.set(state.colorAssignments, id, assignment);
    Vue.set(
      state.assignmentCounts,
      assignment,
      state.assignmentCounts[assignment] + 1
    );
  },
  [types.mutations.RELEASE_COLOR](state, { id, assignment }) {
    Vue.delete(state.colorAssignments, id);
    Vue.set(
      state.assignmentCounts,
      assignment,
      state.assignmentCounts[assignment] - 1
    );
  },
};

/** @type {import("vuex").ActionTree<ColorModuleState, RootState>} */
const actions = {
  [types.actions.ASSIGN_COLOR]({ state, commit }, id) {
    if (state.colorAssignments[id] !== undefined) {
      console.log("skipping color");
      return;
    }

    const lowestAssignmentCount = Math.min(...state.assignmentCounts);

    const assignment = state.assignmentCounts.findIndex(
      (val) => val === lowestAssignmentCount
    );

    commit(types.mutations.ASSIGN_COLOR, { id, assignment });
  },
  [types.actions.RELEASE_COLOR]({ state, commit }, id) {
    if (state.colorAssignments[id] === undefined) {
      return;
    }

    const assignment = state.colorAssignments[id];

    commit(types.mutations.RELEASE_COLOR, { id, assignment });
  },
};

/** @type {import("vuex").Module<ColorModuleState, RootState>} */
const colorModule = {
  state,
  getters,
  mutations,
  actions,
  namespaced: true,
};

export { colorModule, colorTypes, COLOR_NAMESPACE };
