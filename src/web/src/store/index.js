// import local, {localRef} from './local'
import {filterCourses} from "../utils/common";
import {computed, reactive, ref} from 'vue'
import {getCourses, getDefaultSemester, getSemesters, getSubsemesters} from "../plugins/axios/apis";
// import {times} from "../utils/scheduler";
// import {firstHalf, secondHalf, subActivated} from "../utils/subsemester";

// export const semesters = local('semesters', {})
export const semesters = reactive({})

export const currentSemester = ref(null)

getDefaultSemester().then(res => {
    currentSemester.value = res
})

const parseSession = (sessions) => {
    let ret = [0, 0, 0, 0, 0];
    try {
        sessions.forEach((session) => {
            let a = session["time_start"].split(":").map((a) => Number.parseInt(a));
            let b = session["time_end"].split(":").map((a) => Number.parseInt(a));
            const duration = Math.abs(
                (b[0] - a[0]) * 2 + (a[1] < 30 ? 1 : 0) + (b[1] >= 30 ? 1 : 0)
            );
            const end = (21 - b[0]) * 2 + (b[1] < 30 ? 1 : 0);
            const start = (a[0] - 8) * 2 + (a[1] === 30 ? 1 : 0)
            if (start + duration + end !== 28) {
                throw new Error()
            }
            // generate 1 in bits for duration
            let ss = (1 << duration) - 1;
            // placeholder for day of week
            ss <<= end;
            session.time = {start, duration, end}
            ret[session["day_of_week"]] |= ss;
        });
    } catch (e) {
        return [0, 0, 0, 0, 0];
    }
    return ret;
}

const getElapsed = (start, end) => {
    return end.getTime() - start.getTime()
}

getSemesters().then((res) => {
    res.forEach((obj) => {
        getCourses(obj.semester, null).then(courses => {
            const classes = {}
            filterCourses(courses).forEach((course) => {
                const sections = {}
                course.sections.forEach((section, index) => {
                    section.times = parseSession(section.sessions)
                    section.isSelected = false
                    sections[section.crn] = section
                    section.index = index + 1
                })
                course.sections = sections
                course.isSelected = false
                classes[course.name] = course
            })
            // manually track this object
            const semester = reactive({
                courses: classes
            })
            semesters[obj.semester] = semester
            if (obj.semester.toLowerCase().startsWith('summer')) {
                getSubsemesters(obj.semester).then(res => {
                    semester.sub = res.map(subsemester =>
                        [new Date(subsemester.date_start), new Date(subsemester.date_end)]
                    ).sort((l1, l2) => {
                        if (getElapsed(l1[0], l1[1]) < getElapsed(l2[0], l2[1])) return 1
                        return l1[0].getTime() - l2[0].getTime()
                    })
                })
            }
        })
    })
})

export const semester = computed(() => semesters[currentSemester.value] && semesters[currentSemester.value].courses)

export const semester_full = computed(() => semesters[currentSemester.value])

