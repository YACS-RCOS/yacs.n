import {currentSemester, semester, semester_full} from "../store";
import {computed, reactive, ref, watchEffect} from "vue";
import {$notify} from "./notification";
import {occupyColor, unOccupyColor} from "./color";

// helper functions
const generateSchedule = (selections) => {
    let ret = [{
        info: {},
        times: [0, 0, 0, 0, 0]
    }]

    Object.keys(selections).forEach((courseName) => {
        let added = []
        ret.forEach((schedule, index) => {
            added = added.concat(tryAddCourse(schedule, selections[courseName]))
        })
        ret = added
    })
    return ret
}

const tryAddCourse = (schedule, course) => {
    const ret = []
    const sel = Object.keys(course.sections).filter(crn =>
        course.sections[crn].isSelected
    )
    if (!sel.length) {
        throw new Error(course.name + ' has no sections selected!')
    }
    sel.forEach(crn => {
        if (!course.sections[crn].isSelected) return
        const newSchedule = tryAddSection(schedule, course.sections[crn], course)
        if (newSchedule) {
            ret.push(newSchedule)
        }
    })
    return ret
}

const tryAddSection = (schedule, section, course) => {
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

export const findIndex = (start, end) => {
    return semester_full.value.sub.findIndex((l) =>
        new Date(start).getTime() === l[0].getTime() && new Date(end).getTime() === l[1].getTime()
    )
}

// ================================================================================================================== //
/**
 * 0 => not active
 * 1 => first half
 * 2 => second half
 */
export const subActivated = ref(0)
export const subSemesters = ref({
    1: {},
    2: {},
    0: {}
})

export const _selections = ref({})
export const currentSelections = computed(() => {
    const ret = {}
    Object.keys(selections.value).forEach(name => {
        ret[name] = semester.value[name]
    })
    return ret
})

export const firstHalf = computed(() => {
    return Object.assign({}, subSemesters.value['1'], subSemesters.value['0'])
})
export const secondHalf = computed(() => {
    return Object.assign({}, subSemesters.value['2'], subSemesters.value['0'])
})

export const displayedSelections = computed(() => {
    const integratedSelections =
        subActivated.value
            ? Object.assign({}, subSemesters.value['1'], subSemesters.value['2'], subSemesters.value['0'])
            : currentSelections.value

    const ret = {}
    Object.keys(integratedSelections).forEach(name => {
        ret[name] = semester.value[name]
    })
    return ret
})

export const selections = computed(() => {
    switch (subActivated.value) {
        case 1:
            return firstHalf.value
        case 2:
            return secondHalf.value
        case 0:
            return _selections.value
        default:
            console.log('err!')
            return {}
    }
})

export const addCourse = (obj, value) => {
    if (value) {
        obj.color = occupyColor()
    } else {
        unOccupyColor(obj.color.index)
    }
    if (subActivated.value !== 0) {
        let index = findIndex(obj.date_start, obj.date_end).toString()
        if (value) {
            subSemesters.value[index][obj.name] = Object.keys(obj.sections)
        } else {
            delete subSemesters.value[index][obj.name]
        }
    } else {
        if (value) {
            _selections.value[obj.name] = Object.keys(obj.sections)
        } else {
            delete _selections.value[obj.name]
        }
    }
    for (let section in obj.sections) {
        obj.sections[section].isSelected = value
    }
}

watchEffect(() => {
    if (currentSemester.value && currentSemester.value.toLowerCase().startsWith('summer')) {
        subActivated.value = 1
    } else {
        // clear stuff when sub semester not activated
        subSemesters.value = { 1: {}, 2: {}, 0: {} }
        subActivated.value = 0
    }
})

export const currentSchedules = ref([])
export const scheduleIndex = ref(0)

export const currentSchedule = computed(() => currentSchedules.value[scheduleIndex.value] || null)

watchEffect(() => {
    try {
        const generated = generateSchedule(currentSelections.value)
        scheduleIndex.value = 0
        currentSchedules.value = generated
    } catch (e) {
        scheduleIndex.value = -1
        $notify(e.message, 'warning')
    }
})