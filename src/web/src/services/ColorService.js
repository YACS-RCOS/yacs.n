import "@/typedef";
import store from "@/store";

/**
 * Ported over from old YACS
 * Provides colors for schedule blocks
 * @module ColorService
 */

// Default Colors
const COLORS = [
  // H    S    L
  [345, 1, 0.92], // "#ffd4df", red
  [197, 0.88, 0.9], // "#ceeffc", blue
  [46, 1, 0.91], // "#fff4d0", yellow
  [116, 0.64, 0.91], // "#dcf7da", green
  [300, 0.57, 0.93], // "#f7e2f7", purple
  [30, 0.28, 0.9], // "#ede6df", brown
  [33, 1, 0.91], // "#ffe9cf", orange
  [304, 1, 0.91], // "#ffd1fc", pink
  [178, 0.9, 0.92], // "#d9fdfc", aquamarine
  [0, 0.29, 0.9], // "#e2caca", maroon, changed
  [197, 0.51, 0.85], // "#a3cfe1", dark blue, changed
  [116, 0.41, 0.85], // "#acdba9", dark green, changed
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
  [341, 1, 0.56], // "#ff2066", red
  [197, 1, 0.47], // "#00aff2", blue
  [43, 1, 0.64], // "#ffcb45", yellow
  [127, 0.66, 0.57], // "#48da58", green
  [296, 0.58, 0.65], // "#d373da", purple
  [30, 0.26, 0.52], // "#a48363", brown
  [28, 1, 0.6], // "#ff9332", orange
  [304, 1, 0.5], // "#ff00ef", pink
  [179, 1, 0.5], // "#00fff9", aquamarine
  [0, 1, 0.37], // "#ab0000", maroon, changed
  [205, 0.99, 0.36], // "#015fa2", dark blue, changed
  [126, 0.55, 0.38], // "#298e33", dark green, changed
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
  [358, 0.96, 0.6], // "#fb373e", red
  [208, 0.61, 0.72], // "#8cbbe3", blue
  [57, 0.91, 0.65], // "#f7f056", yellow
  [85, 0.46, 0.77], // "#cae0ab", green
  [286, 0.26, 0.84], // "#dccce1", purple
  [30, 0.28, 0.9], // "#ede6df", brown
  [42, 0.91, 0.61], // "#f6c141", orange
  [303, 1, 0.96], // "#ffebfe", pink
  [212, 0.51, 0.6], // "#6596cd", aquamarine
  [0, 0.29, 0.84], // "#e2caca", maroon
  [196, 0.67, 0.55], // "#2286aa", dark blue, changed
  [112, 0.38, 0.66], // "#90c987", dark green
];
const COLOR_BLIND_BORDER_COLORS = [
  [341, 1, 0.32], //"#a30034", red
  [197, 1, 0.47], //"#00aff2", blue
  [43, 1, 0.64], //"#ffcb45", yellow
  [85, 0.46, 0.56], //"#97c25b", green
  [296, 0.58, 0.65], //"#d373da", purple
  [30, 0.26, 0.52], //"#a48363", brown
  [28, 1, 0.6], //"#ff9332", orange
  [304, 1, 0.84], //"#ffadfa", pink
  [212, 0.51, 0.4], //"#32639a", aquamarine
  [0, 1, 0.34], //"#ab0000", maroon
  [205, 0.99, 0.32], //"#015fa2", dark blue
  [126, 0.55, 0.36], //"#298e33", dark green
];

const NUM_COLORS = 12;

// TODO: use something persistent
var assignmentIncr = 0;
var colorAssignments = new Map();

const _toHslStr = (lst, sOffset = 0, lOffset = 0) => {
  return (
    "hsl(" +
    lst[0].toString() +
    "," +
    ((lst[1] + sOffset) * 100).toString() +
    "%," +
    ((lst[2] + lOffset) * 100).toString() +
    "%)"
  );
};

const _getColor = (id) => {
  const assignment = _assign(id);
  if (store.getters.colorBlindAssistState && store.getters.darkModeState) {
    return {
      primary: _toHslStr(COLOR_BLIND_COLORS[assignment], 0, -0.37),
      text: "#fff",
      border: _toHslStr(COLOR_BLIND_BORDER_COLORS[assignment], -0.05, 0),
    };
  } else if (store.getters.colorBlindAssistState) {
    return {
      primary: _toHslStr(COLOR_BLIND_COLORS[assignment]),
      text: "#000",
      border: _toHslStr(COLOR_BLIND_BORDER_COLORS[assignment]),
    };
  } else if (store.getters.darkModeState) {
    return {
      primary: _toHslStr(COLORS[assignment], -0.07, -0.67),
      text: _toHslStr(TEXT_COLORS[assignment], -0.17, 0.27),
      border: _toHslStr(BORDER_COLORS[assignment], -0.13, -0.11),
    };
  } else {
    return {
      primary: _toHslStr(COLORS[assignment]),
      text: _toHslStr(TEXT_COLORS[assignment]),
      border: _toHslStr(BORDER_COLORS[assignment]),
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
  return _getColor(courseSession).primary;
};
/**
 * Returns the border color associated with `courseSession`
 * @param {CourseSession} courseSession
 * @returns {string} hex color code
 */
export const getBorderColor = (courseSession) => {
  return _getColor(courseSession).border;
};
/**
 * Returns the text color associated with `courseSession`
 * @param {CourseSession} courseSession
 * @returns {string} hex color code
 */
export const getTextColor = (courseSession) => {
  return _getColor(courseSession).text;
};
