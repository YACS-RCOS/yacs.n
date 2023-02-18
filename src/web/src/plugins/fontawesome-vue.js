import Vue from "vue";

import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// This allows for tree-shaking to minimize bundle size
import {
  faPaperPlane,
  faMoon,
  faCalendar,
  faList,
  faBars,
  faSearch
} from "@fortawesome/free-solid-svg-icons";

library.add(faPaperPlane, faMoon, faCalendar, faList, faBars, faSearch);

Vue.component("font-awesome-icon", FontAwesomeIcon);
