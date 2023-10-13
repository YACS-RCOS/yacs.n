import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// This allows for tree-shaking to minimize bundle size
import {
  faAddressBook,
  faBars,
  faCalendar,
  faFileAlt,
  faList,
  faMoon,
  faPaperPlane,
  faSearch,
} from "@fortawesome/free-solid-svg-icons";

library.add(
  faPaperPlane,
  faMoon,
  faCalendar,
  faList,
  faBars,
  faSearch,
  faAddressBook,
  faFileAlt,
);

export default FontAwesomeIcon;
