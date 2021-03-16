import "@/typedef";

/**
 * Ported over from old YACS
 * Provides colors for schedule blocks
 * @module ColorService
 */

//text and background should be very similar
//color should be a light shade of the color of text

const COLORS = [
  "#ffd4df", //red
  "#ceeffc", //blue
  "#fff4d0", //yellow
  "#dcf7da", //green
  "#f7e2f7", //purple
  "#ede6df", //brown
  "#ffe9cf", //orange
  "#fed7fc", //pink done
  "#a4f9f7", //aquamarine
  "#ad6666", //maroon
  "#A3CFE1", //dark blue
  "#ACDBA9", //dark green
];
const TEXT_COLORS = [
  "#d1265d",
  "#1577aa",
  "#bf8a2e",
  "#008a2e",
  "#853d80",
  "#9d5733",
  "#d9652b",
  "#ff00ef",
  "#04776f",
  "#ab1111",
  "#014779",
  "#116940",
  // make all black to help with visibility???
  // apparently out site fails this test https://wave.webaim.org/
  // which helps site stay accessible to people with disabilities
  // add a switch to make the text black
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

const NUM_COLORS = 12;

// TODO: use something persistent
var assignmentIncr = 0;
var colorAssignments = new Map();

const _getColor = (id) => {
  const assignment = _assign(id);
  return {
    primary: COLORS[assignment],
    text: TEXT_COLORS[assignment],
    border: BORDER_COLORS[assignment],
  };
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
