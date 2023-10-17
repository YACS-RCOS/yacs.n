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
  faSearch,
  faAddressBook,
  faFileAlt,
  faQuestionCircle,
  // faAddressBook,
} from "@fortawesome/free-solid-svg-icons";

library.add(
  faQuestionCircle,
  faPaperPlane,
  faMoon,
  faCalendar,
  faList,
  faBars,
  faSearch,
  faAddressBook,
  faFileAlt,
  faFileAlt
);

Vue.component("font-awesome-icon", FontAwesomeIcon);
