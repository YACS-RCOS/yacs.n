/** @module store/user */

import Vue from "vue";

import { client } from "@/plugins/axios";

import { prefixNamespacedTypes } from "@/utils";

const USER_SESSION_ID_COOKIE_KEY = "sessionID";

const {
  namespace: USER_NAMESPACE,
  local: types,
  ...userTypes
} = prefixNamespacedTypes("user", {
  state: {
    SESSION_ID: "sessionId",
    USER: "user",
  },
  getters: {
    IS_LOGGED_IN: "isLoggedIn",
    CURRENT_USER_INFO: "currentUserInfo",
  },
  mutations: {
    SET_USER_INFO: "setUserInfo",
    SET_SESSION_ID: "setSessionId",
  },
  actions: {
    LOGIN: "login",
    LOGOUT: "logout",
    LOAD_SESSION_COOKIE: "loadSessionCookie",
    LOAD_USER_INFO: "loadUserInfo",
  },
});

/**
 * @typedef {import("../index").RootState} RootState
 * @typedef UserModuleState
 * @property {string|null} sessionId
 * @property {import("@/typedef").User|null} user
 */

/** @type {UserModuleState} */
const state = {
  sessionId: null,
  user: null,
};

/** @type {import("vuex").GetterTree<UserModuleState, RootState>} */
const getters = {
  [types.getters.IS_LOGGED_IN]: (state) => state.sessionId !== null,
  [types.getters.CURRENT_USER_INFO]: (state, getters) =>
    !getters.isLoggedIn ? null : state.user,
};

/** @type {import("vuex").MutationTree<UserModuleState>} */
const mutations = {
  [types.mutations.SET_USER_INFO](state, user) {
    if (user === null) {
      state.user = null;
    } else {
      state.user = { ...state.user, ...user };
    }
  },
  [types.mutations.SET_SESSION_ID](state, sessionId) {
    state.sessionId = sessionId;
  },
};

/** @type {import("vuex").ActionTree<UserModuleState, RootState>} */
const actions = {
  async [types.actions.LOAD_SESSION_COOKIE]({ commit, dispatch }) {
    if (!Vue.$cookies.isKey(USER_SESSION_ID_COOKIE_KEY)) {
      return;
    }

    const sessionId = Vue.$cookies.get(USER_SESSION_ID_COOKIE_KEY);

    await dispatch(types.actions.LOAD_USER_INFO, sessionId);

    commit(types.mutations.SET_SESSION_ID, sessionId);
  },
  async [types.actions.LOGIN]({ commit, dispatch, getters }, userInfo) {
    if (getters[types.getters.IS_LOGGED_IN]) {
      return;
    }

    const response = await client.post("/session", userInfo);

    const {
      data: { success, errMsg, content },
    } = response;

    if (!success) {
      throw errMsg || "Unknown error";
    }

    await dispatch(types.actions.LOAD_USER_INFO, content.sessionID);

    Vue.$cookies.set(USER_SESSION_ID_COOKIE_KEY, content.sessionID);

    commit(types.mutations.SET_SESSION_ID, content.sessionID);
  },
  async [types.actions.LOAD_USER_INFO](
    { commit, dispatch, getters },
    sessionId
  ) {
    try {
      const {
        data: { success, errMsg, content },
      } = await client.get(`/user/${sessionId}`);

      if (!success) {
        throw errMsg || "Unknown error";
      }

      commit(types.mutations.SET_USER_INFO, content);
    } catch (err) {
      if (getters[types.getters.IS_LOGGED_IN]) {
        // session expired/mismatch/whatever
        await dispatch(types.actions.LOGOUT, { deleteSession: false });
      }

      throw err;
    }
  },
  async [types.actions.LOGOUT]({ state, commit, getters }, options) {
    if (!getters[types.getters.IS_LOGGED_IN]) {
      return;
    }

    if (
      options === undefined ||
      options.deleteSession === undefined ||
      options.deleteSession === true
    ) {
      const {
        data: { success, errMsg },
      } = await client.delete("/session", {
        data: {
          sessionID: state.sessionId,
        },
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!success) {
        throw errMsg || "Unknown error";
      }
    }

    commit(types.mutations.SET_SESSION_ID, null);
    commit(types.mutations.SET_USER_INFO, null);

    Vue.$cookies.remove(USER_SESSION_ID_COOKIE_KEY);
  },
};

/** @type {import("vuex").Module<UserModuleState, RootState>} */
const userModule = {
  state,
  getters,
  mutations,
  actions,
  namespaced: true,
};

export { userModule, userTypes, USER_NAMESPACE };
