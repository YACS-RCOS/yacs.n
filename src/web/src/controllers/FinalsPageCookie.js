import "@/typedef";

// eslint-disable-next-line no-unused-vars
import {VueCookies} from "vue-cookies";

const COOKIE_KEY = "finalExams";

class FinalsPageCookie {
    /**
     * @param {VueCookies} $cookies
    */

    constructor($cookies, exams) {
        this.$cookies = $cookies;
        this.exams = exams;
    }

    /**
     * @param {VueCookies} $cookies
    */
    static load($cookies) {// key = COOKIE_KEY
        return new FinalsPageCookie($cookies, $cookies.isKey(COOKIE_KEY) ? $cookies.get(COOKIE_KEY) : []);
    }

    /**
   * Save current state into cookie
   * @param {string} key defaults to `COOKIE_KEY`
   */
    save(key = COOKIE_KEY) {
        this.$cookies.set(key, this.exams);
    }

    clear() {
        this.exams = [];
        return this;
    }

    /**
   *
   * @returns {exams} list of selected courses
   * of current semester
   */
    getExams() {
        return this.exams;
    }

    setExams(exams) {
        this.exams = exams;
        this.save()
    }


    // /**
    //  * Only adds an entry for the course, to add sections, call `addCourseSection`
    //  * @param {String} Department
    //  * @param {String} CourseCode
    //  * @param {String} Section
    //  * @param {String} Day
    //  * @returns {this}
    //  */
    // addCourse(Department, CourseCode, Section, Day) {
    //     const course = {
    //         Department,
    //         CourseCode,
    //         Section,
    //         Day,
    //     };
    //     this.exams.push(course);
    //     return this;
    // }
}

export {
    FinalsPageCookie
};
