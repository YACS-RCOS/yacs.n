import { computed, ref } from "vue";
import {currentSelections} from "./selection";
import {currentSemester} from "./semester";

// helper functions
const generateSchedule = (selections) => {
    let ret = [{
        info: {},
        times: [0, 0, 0, 0, 0]
    }]

    Object.keys(selections).forEach((courseName) => {
        let added = []
        ret.forEach((schedule) => {
            added = added.concat(tryAddCourse(schedule, selections[courseName]))
        })
        ret = added
    })
    return ret
}

const tryAddCourse = (schedule, course) => {
    const ret = []
    Object.keys(course.sections).forEach(crn => {
        const newSchedule = tryAddSection(schedule, course, course.sections[crn])
        if (newSchedule) {
            ret.push(newSchedule)
        }
    })
    return ret
}

const tryAddSection = (schedule, course, section) => {
    const newSchedule = JSON.parse(JSON.stringify(schedule))
    for (let i = 0; i < 5; i++) {
        if ((newSchedule.times[i] & section.times[i]) > 0) {
            return null
        } else {
            newSchedule.times[i] |= section.times[i]
        }
    }
    newSchedule.info[course.name] = { course, section }
    return newSchedule
}

export const currentSchedules = computed(() => {
    return generateSchedule(currentSelections.value)
})

export const scheduleIndex = ref(0)

export const currentSchedule = computed(() => {
    return currentSchedules.value[scheduleIndex.value] || null
})