import "@/typedef";
import store from "@/store";

/**
 * Ported over from old YACS
 * Provides colors for schedule blocks
 * @module ColorService
 */

//Default Colors
const COLORS = [
  "#ffd4df", //red
  "#ceeffc", //blue
  "#fff4d0", //yellow
  "#dcf7da", //green
  "#f7e2f7", //purple
  "#ede6df", //brown
  "#ffe9cf", //orange
  "#ffd1fc", //pink
  "#d9fdfc", //aquamarine
  "#e2caca", //maroon
  "#A3CFE1", //dark blue
  "#ACDBA9", //dark green
];
const TEXT_COLORS = [
  "#86193B", //red
  "#0C4C6E", //blue
  "#6B4D1A", //yellow
  "#005C1F", //green
  "#70336C", //purple
  "#703D23", //brown
  "#7E3815", //orange
  "#800077", //pink
  "#005C56", //aquamarine
  "#7D0C0C", //maroon
  "#014779", //dark blue
  "#084429", //dark green
];
const BORDER_COLORS = [
  "#ff2066",
  "#00aff2",
  "#ffcb45",
  "#48da58",
  "#d373da",
  "#a48363",
  "#ff9332",
  "#ff00ef",
  "#00fff9",
  "#ab0000",
  "#015FA2",
  "#298E33",
];

//Dark Mode Colors
const DARK_MODE_COLORS = [
  "#D29BA9", //red
  "#A1C3D0", //blue
  "#EBDEB4", //yellow
  "#B7DAB4", //green
  "#DFC0DF", //purple
  "#D8C9B9", //brown
  "#DFC7AC", //orange
  "#E4B7E1", //pink
  "#ABD9D8", //aquamarine
  "#CAA5A5", //maroon
  "#A3CFE1", //dark blue
  "#9ED59A", //dark green
];
const DARK_MODE_TEXT_COLORS = [
  "#9B465B",
  "#1577aa",
  "#bf8a2e",
  "#008a2e",
  "#853d80",
  "#9d5733",
  "#C17F33",
  "#BC4EB4",
  "#00a499",
  "#ab1111",
  "#014779",
  "#116940",
];
const DARK_MODE_BORDER_COLORS = [
  "#A94C63",
  "#528CA3",
  "#D4B95E",
  "#6EB569",
  "#d373da",
  "#a48363",
  "#C69D6C",
  "#D897D5",
  "#56B3B2",
  "#ab0000",
  "#015FA2",
  "#298E33",
];

/**
 * Color Blind Friendly Colors
 *
 * Adapted from Paul Tot's discrete rainbow scheme
 * https://personal.sron.nl/~pault/#fig:scheme_rainbow_discrete
 *
 * Colors adjusted using https://davidmathlogic.com/colorblind/
 *
 * Color palette tested using
 * https://www.color-blindness.com/coblis-color-blindness-simulator/
 */
const COLOR_BLIND_COLORS = [
  "#FB373E", //red
  "#8CBBE3", //blue
  "#F7F056", //yellow
  "#CAE0AB", //green
  "#DCCCE1", //purple
  "#ede6df", //brown
  "#F6C141", //orange
  "#FFEBFE", //pink
  "#6596CD", //aquamarine
  "#e2caca", //maroon
  "#2286AA", //dark blue
  "#90C987", //dark green
];
const COLOR_BLIND_TEXT_COLORS = [
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
  "#000000",
];
const COLOR_BLIND_BORDER_COLORS = [
  "#A30034",
  "#00aff2",
  "#ffcb45",
  "#97C25B",
  "#d373da",
  "#a48363",
  "#ff9332",
  "#FFADFA",
  "#32639A",
  "#ab0000",
  "#015FA2",
  "#298E33",
];

const NUM_COLORS = 12;

// TODO: use something persistent
var assignmentIncr = 0;
var colorAssignments = new Map();

const _getColor = (id) => {
  const assignment = _assign(id);
  if (store.getters.colorBlindAssistState) {
    return {
      primary: COLOR_BLIND_COLORS[assignment],
      text: COLOR_BLIND_TEXT_COLORS[assignment],
      border: COLOR_BLIND_BORDER_COLORS[assignment],
    };
  } else if (store.getters.darkModeState) {
    return {
      primary: DARK_MODE_COLORS[assignment],
      text: DARK_MODE_TEXT_COLORS[assignment],
      border: DARK_MODE_BORDER_COLORS[assignment],
    };
  } else {
    return {
      primary: COLORS[assignment],
      text: TEXT_COLORS[assignment],
      border: BORDER_COLORS[assignment],
    };
  }
};

const _assign = (id) => {
  if (colorAssignments.has(id)) return colorAssignments.get(id);
  else return colorAssignments.set(id, _nextAssignment()).get(id);
};

const _nextAssignment = () => {
  return ++assignmentIncr % NUM_COLORS;
};
/**
 * Returns the background color associated with `courseSession`
 * @param {CourseSession} courseSession
 * @returns {string} Hex color code
 */
export const getBackgroundColor = (courseSession) => {
  return _getColor(courseSession.crn).primary;
};
/**
 * Returns the border color associated with `courseSession`
 * @param {CourseSession} courseSession
 * @returns {string} hex color code
 */
export const getBorderColor = (courseSession) => {
  return _getColor(courseSession.crn).border;
};
/**
 * Returns the text color associated with `courseSession`
 * @param {CourseSession} courseSession
 * @returns {string} hex color code
 */
export const getTextColor = (courseSession) => {
  return _getColor(courseSession.crn).text;
};
