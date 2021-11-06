import "@/typedef";

// eslint-disable-next-line no-unused-vars
import { VueCookies } from "vue-cookies";

const COOKIE_KEY = "selectedIndex";

/**
 * Module for managing selected index cookie
 * Mostly copied from SelectedCoursesCookie
 *
 * @example
 * SelectedCoursesCookie
 *  .load(this.$cookies)
 *  .semester(semester)
 *  .updateIndex(newIndex)
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
   * Load saved selected index from cookie
   * @param {VueCookies} $cookies
   * @param {string} key defaults to `COOKIE_KEY`
   * @returns {SelectedIndexCookie}
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
   * @example SelectedIndexCookie.load(this.$cookies).clear().save()
   */
  clear() {
    this._selectedSemestersIndex = {};

    return this;
  }

  /**
   *
   * @returns {int} index of current semester
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

  //Updates index of current semester
  updateIndex(newIndex) {
    if (this._semester === undefined) {
        return this;
    }

    this._selectedSemestersIndex[this._semester] = newIndex;

    return this;
  }
}

export { SelectedIndexCookie };
