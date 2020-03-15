/**
 * @typedef {import('@/index').CourseSession} CourseSession
 */
/** */
const COLORS = ['#ffd4df', '#ceeffc', '#fff4d0', '#dcf7da', '#f7e2f7', '#ede6df', '#ffe9cf'];
const TEXT_COLORS = ['#d1265d', '#1577aa', '#bf8a2e', '#008a2e', '#853d80', '#9d5733', '#d9652b'];
const BORDER_COLORS = ['#ff2066', '#00aff2', '#ffcb45', '#48da58', '#d373da', '#a48363', '#ff9332'];
const NUM_COLORS = 7;

// TODO: use something persistent
var assignmentIncr = 0;
var colorAssignments = new Map();

/**
 * @module ColorService
 * Ported over from old YACS
 * Provides colors for schedule blocks
 */
export default {
  /**
   * @private
   * @param {number} id
   */
  _getColor(id) {
    const assignment = this._assign(id);
    return {
      primary: COLORS[assignment],
      text: TEXT_COLORS[assignment],
      border: BORDER_COLORS[assignment]
    };
  },
  /**
   * @private
   * @param {number} id
   */
  _assign(id) {
    if (colorAssignments.has(id)) return colorAssignments.get(id);
    else return colorAssignments.set(id, this._nextAssignment()).get(id);
  },
  /**
   * @private
   */
  _nextAssignment() {
    return ++assignmentIncr % NUM_COLORS;
  },
  /**
   * Returns the background color associated with `courseSession`
   * @param {CourseSession} courseSession
   * @returns {string} Hex color code
   */
  getBackgroundColor(courseSession) {
    return this._getColor(courseSession.crn).primary;
  },
  /**
   * Returns the border color associated with `courseSession`
   * @param {CourseSession} courseSession
   * @returns {string} hex color code
   */
  getBorderColor(courseSession) {
    return this._getColor(courseSession.crn).border;
  },
  /**
   * Returns the text color associated with `courseSession`
   * @param {CourseSession} courseSession
   * @returns {string} hex color code
   */
  getTextColor(courseSession) {
    return this._getColor(courseSession.crn).text;
  }
};
