// import local, {localRef} from './local'
import {filterCourses} from "../utils/common";
import {computed, reactive, ref} from 'vue'
import {getCourses, getDefaultSemester, getSemesters} from "../plugins/axios/apis";

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
            const end = (20 - b[0]) * 2 + (b[1] < 30 ? 1 : 0);
            // generate 1 in bits for duration
            let ss = (1 << duration) - 1;
            // placeholder for day of week
            ss <<= end;
            ret[session["day_of_week"]] |= ss;
        });
    } catch (e) {
        return [0, 0, 0, 0, 0];
    }
    return ret;
}

getSemesters().then((res) => {
    res.forEach((obj) => {
        getCourses(obj.semester, null).then(courses => {
            const classes = {}
            filterCourses(courses).forEach((course) => {
                const sections = {}
                course.sections.forEach(section => {
                    section.times = parseSession(section.sessions)
                    section.isSelected = false
                    sections[section.crn] = section
                })
                course.sections = sections
                course.isSelected = false
                classes[course.name] = course
            })
            semesters[obj.semester] = classes
        })
    })
})

export const semester = computed(() => semesters[currentSemester.value])

export const selections = reactive({})

export const currentSelections = computed(() => {
    const ret = {}
    Object.keys(selections).forEach(name => {
        ret[name] = semester.value[name]
    })
    return ret
})
