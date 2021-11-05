import "@/typedef";

// eslint-disable-next-line no-unused-vars
import { VueCookies } from "vue-cookies";

const COOKIE_KEY = "selectedIndex";

/**
 * Handy module for managing selected courses cookie storage
 *
 * @example
 * SelectedCoursesCookie
 *  .load(this.$cookies)
 *  .semester(semester)
 *  .addCourse(course)
 *  .save()
 */
class SelectedIndexCookie {
  /**
   * @typedef SelectedSemestersIndex
   * @type {{[semester: string]: int}}
   */

  /**
   * @param {VueCookies} $cookies
   * @param {SelectedSemestersIndex} selectedSemestersIndex
   * @private
   */
  constructor($cookies, selectedSemestersIndex) {
    /**
     * @type {VueCookies}
     * @private
     */
    this.$cookies = $cookies;
    /**
     * @type {SelectedSemestersIndex}
     * @private
     */
    this._selectedSemestersIndex = selectedSemestersIndex;
    /**
     * @type {string}
     * @private
     */
    this._semester = undefined;
  }

  /**
   * Load saved selected courses from cookie
   * @param {VueCookies} $cookies
   * @param {string} key defaults to `COOKIE_KEY`
   * @returns {SelectedCoursesCookie}
   */
  static load($cookies, key = COOKIE_KEY) {
    return new SelectedIndexCookie(
      $cookies,
      $cookies.isKey(key) ? $cookies.get(key) : {}
    );
  }

  /**
   * Save current state into cookie
   * @param {string} key defaults to `COOKIE_KEY`
   */
  save(key = COOKIE_KEY) {
    this.$cookies.set(key, this._selectedSemestersIndex);
  }

  /**
   * Set semester context for subsequent actions. Must be
   * called before executing other actions.
   * @example
   * // Load `course1` into semester `Fall 2020` and `course2`
   * //  into `Spring 2021`
   * SelectedCoursesCookie.load(this.$cookies)
   *  .semester("FALL 2020")
   *    .addCourse(course1)
   *  .semester("SPRING 2021")
   *    .removeCourse(course2)
   *  .save()
   * @param {string} semester
   * @returns {this}
   */
  semester(semester) {
    this._semester = semester;

    return this;
  }

  /**
   * Reset state to empty. Useful for resetting cookie
   *
   * @example SelectedCoursesCookie.load(this.$cookies).clear().save()
   */
  clear() {
    this._selectedSemestersIndex = {};

    return this;
  }

  /**
   *
   * @returns {SelectedCourse[]} list of selected courses
   * of current semester
   */
  get selectedIndex() {
    if (this._semester === undefined) {
      return 0;
    }

    if (this._selectedSemestersIndex[this._semester] === undefined) {
      this._selectedSemestersIndex[this._semester] = 0;
    }

    return this._selectedSemestersIndex[this._semester];
  }

  updateIndex(newIndex) {
    if (this._semester === undefined) {
        return this;
    }

    this._selectedSemestersIndex[this._semester] = newIndex;

    return this;
  }
}

export { SelectedIndexCookie };
