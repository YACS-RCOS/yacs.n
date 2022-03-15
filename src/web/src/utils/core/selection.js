import {computed, reactive, ref, watch} from "vue";
import {currentSemester, currentSemesterName, getSubByTime, subSemester} from "./semester";
import {occupyColor, unOccupyColor} from "../color";

const getCurrent = (selections) => {
    const ret = {}
    Object.keys(selections).forEach((courseName) => {
        const courseInfo = Object.assign({}, currentSemester.value.courses[courseName])
        const temp = {}
        selections[courseName].forEach(crn => {
            temp[crn] = courseInfo.sections[crn]
        })
        courseInfo.sections = selections[courseName].length ? temp : undefined
        ret[courseName] = courseInfo
    })
    return ret
}

watch(() => currentSemesterName.value, () => {
    _selections.first = {}
    _selections.second = {}
    _selections.full = {}
})

// manipulations should be done here
const _selections = reactive({
    first: {},
    second: {},
    full: {}
})

export const dedicatedSelections = computed(() => {
    return _selections[subSemester.value]
})
export const currentDedicatedSelections = computed(() => {
    return getCurrent(dedicatedSelections.value)
})
export const generalSelections = computed(() => {
    return _selections.full
})
export const currentGeneralSelections = computed(() => {
    return getCurrent(generalSelections.value)
})
export const shadowSelections = computed(() => {
    if (subSemester.value === 'first') {
        return _selections.second
    } else if (subSemester.value === 'second') {
        return _selections.first
    }
    return {}
})
export const currentShadowSelections = computed(() => {
    return getCurrent(shadowSelections.value)
})

export const selections = computed(() => {
    if (subSemester.value !== 'full')
        return Object.assign({}, _selections[subSemester.value], _selections.full)
    return _selections.full
})
export const currentSelections = computed(() => {
    return getCurrent(selections.value)
})

export const displayedSelections = computed(() =>
    Object.assign({}, _selections.first, _selections.second, _selections.full)
)

export const toggleCourse = (courseInfo, value) => {
    // debugger
    if (value) {
        courseInfo.color = occupyColor()
    } else {
        unOccupyColor(courseInfo.color.index)
    }
    const sub = getSubByTime(new Date(courseInfo.date_start), new Date(courseInfo.date_end))
    courseInfo.sub = sub
    if (value)
        _selections[sub][courseInfo.name] = Object.keys(courseInfo.sections)
    else
        delete _selections[sub][courseInfo.name]
}

export const toggleSection = (courseInfo, crn, value) => {
    const sub = courseInfo.sub
    if (value) {
        _selections[sub][courseInfo.name].push(crn)
    } else {
        const index = _selections[sub][courseInfo.name].indexOf(crn)
        _selections[sub][courseInfo.name].splice(index, 1)
    }

}