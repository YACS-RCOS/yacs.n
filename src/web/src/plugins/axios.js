import axios from "axios";

import Vue from "vue";

export const client = axios.create({
  baseURL: "/api",
});

Vue.use({
  install(Vue) {
    Vue.prototype.$axios = client;
    Vue.$axios = client;
  },
});
