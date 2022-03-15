import { computed, ref } from "vue";
import {
    currentDedicatedSelections,
    currentGeneralSelections,
    currentSelections, currentShadowSelections,
    dedicatedSelections
} from "./selection";
import {currentSemester, subSemester} from "./semester";

// helper functions
const generateSchedule = (dedicated, shadow, general) => {
    let ret = [{
        info: {},
        times: [[], [], [], [], []],
        times_shadow: [[], [], [], [], []]
    }]

    Object.keys(dedicated).forEach((courseName) => {
        let added = []
        ret.forEach((schedule) => {
            added = added.concat(tryAddCourse(schedule, dedicated[courseName]))
        })
        ret = added
    })
    if (subSemester.value === 'full')
        return ret
    Object.keys(shadow).forEach((courseName) => {
        let added = []
        ret.forEach((schedule) => {
            added = added.concat(tryAddCourse(schedule, shadow[courseName], 'shadow'))
        })
        ret = added
    })
    Object.keys(general).forEach((courseName) => {
        let added = []
        ret.forEach((schedule) => {
            added = added.concat(tryAddCourse(schedule, general[courseName], 'full'))
        })
        ret = added
    })
    return ret
}

const tryAddCourse = (schedule, course, flag='') => {
    const ret = []
    Object.keys(course.sections).forEach(crn => {
        const newSchedule = tryAddSection(schedule, course, course.sections[crn], flag)
        if (newSchedule) {
            ret.push(newSchedule)
        }
    })
    return ret
}

const conflict = (section, schedule) => {
    let ret = true
    for (let i = 0; i < 5; i++) {
        ret &= schedule[i].every(([s1, e1]) => {
            const [s2, e2] = section[i]
            return s2 > e1 || s1 > e2
        })
    }
    return ret
}

const addition = (section, schedule) => {
    const ret = []
    for (let i = 0; i < 5; i++) {
        console.log(schedule[i], section[i])
        ret.push(schedule[i].concat(section[i]))
    }
    return ret
}

const tryAddSection = (schedule, course, section, flag) => {
    const newSchedule = Object.assign({}, schedule)

    if (flag === '') {
        if (!conflict(section.times, newSchedule.times)) {
            return null
        } else {
            newSchedule.times = addition(section.times, newSchedule.times)
        }
    } else if (flag === 'full') {
        if (!conflict(section.times, newSchedule.times) || !conflict(section.times, newSchedule.times_shadow)) {
            return null
        } else {
            newSchedule.times = addition(section.times, newSchedule.times)
            newSchedule.times_shadow = addition(section.times, newSchedule.times_shadow)
        }
    } else {
        if (!conflict(section.times, newSchedule.times_shadow)) {
            return null
        } else {
            newSchedule.times = addition(section.times, newSchedule.times_shadow)
        }
    }
    if (flag !== 'shadow')
        newSchedule.info[course.name] = { course, section }
    console.log(section)
    return newSchedule
}

export const currentSchedules = computed(() => {
    return generateSchedule(currentDedicatedSelections.value, currentShadowSelections.value, currentGeneralSelections.value)
})

export const scheduleIndex = ref(0)

export const currentSchedule = computed(() => {
    return currentSchedules.value[scheduleIndex.value] || null
})