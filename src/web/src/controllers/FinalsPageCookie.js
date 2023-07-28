import "@/typedef";

// eslint-disable-next-line no-unused-vars
import {VueCookies} from "vue-cookies";

const COOKIE_KEY = "finalExams";

class FinalsPageCookie {

    constructor($cookies, exams) {
        this.$cookies = $cookies;
        this.exams = exams; // Initialize as empty array
    }



    static load($cookies) {// key = COOKIE_KEY
        // console.log("load: ", this.getExams());
        // return new FinalsPageCookie($cookies);
        let exams = $cookies.isKey(COOKIE_KEY) ? $cookies.get(COOKIE_KEY) : [];
        if (!Array.isArray(exams)){
            exams = [];
        }
        return new FinalsPageCookie($cookies, exams);
    }

    save(key = COOKIE_KEY) {
        this.$cookies.set(key, this.exams);
    }

    clear() {
        this.exams = [];
        return this;
    }


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
