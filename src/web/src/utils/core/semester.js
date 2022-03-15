import {computed, reactive, ref, watch} from 'vue'
import {getCourses, getDefaultSemester, getSemesters, getSubsemesters} from "../../plugins/axios/apis";
import {filterCourses} from "../common";

const parseSession = (sessions) => {
    let ret = [[], [], [], [], []];
    try {
        sessions.forEach((session) => {
            const [s_h, s_m, s_s] = session["time_start"].split(":").map((a) => Number.parseInt(a));
            const [e_h, e_m, e_s] = session["time_end"].split(":").map((a) => Number.parseInt(a));
            const start = new Date()
            const end = new Date()
            start.setTime(((s_h * 60 + s_m) * 60 + s_s) * 1000)
            end.setTime(((e_h * 60 + e_m) * 60 + e_s) * 1000)
            session.time = [start, end]
            ret[session["day_of_week"]].push([start, end])
        });
    } catch (e) {
        return [[], [], [], [], []];
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
