import {computed, reactive, ref, watch} from 'vue'
import {getCourses, getDefaultSemester, getSemesters, getSubsemesters} from "../../plugins/axios/apis";
import {filterCourses} from "../common";

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

export const semesters = reactive({})
export const currentSemesterName = ref('')
export const currentSemester = computed(() => semesters[currentSemesterName.value])

getSemesters().then(({data}) => {
    data.forEach(obj => {
        getCourses(obj.semester, null).then(({data: courses}) => {
            // manually track this object
            const semester = reactive({
                courses: {}
            })
            filterCourses(courses).forEach((course) => {
                const newSections = {}
                course.sections.forEach((section, sectionIndex) => {
                    section.times = parseSession(section.sessions)
                    section.isSelected = false
                    section.index = sectionIndex + 1
                    newSections[section.crn] = section
                })
                course.sections = newSections
                course.isSelected = false
                semester.courses[course.name] = course
            })
            semesters[obj.semester] = semester
            console.log(semesters)
            if (obj.semester.toLowerCase().startsWith('summer')) {
                getSubsemesters(obj.semester).then(({data: subs}) => {
                    const newSubs = subs.map(sub => [new Date(sub.date_start), new Date(sub.date_end)]).sort((a,b) => {
                        return a[0] - b[0] || getElapsed(b[0], b[1]) - getElapsed(a[0], a[1])
                    })
                    semester.sub = {
                        full: newSubs[0],
                        first: newSubs[1],
                        second: newSubs[2],
                    }
                })
            }
        })
    })
}).finally(() => {
    getDefaultSemester().then(({data}) => {
        currentSemesterName.value = data
    })
})

const subSemesters = computed(() => {
    const ret = {}
    Object.keys(semesters).forEach(semester => {
        ret[semester] = semesters[semester].sub
    })
    return ret
})

export const subSemester = ref('full')

const currentSubSemester = computed(() =>
    subSemesters.value[currentSemesterName.value]
)

export const getSubByTime = (start, end) => {
    if (!currentSubSemester.value)
        return 'full'
    for (const sub in currentSubSemester.value) {
        const [a, b] = currentSubSemester.value[sub]
        if (getElapsed(start, a) === 0 && getElapsed(end, b) === 0) {
            return sub
        }
    }
    return 'full'
}