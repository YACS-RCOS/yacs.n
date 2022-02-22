import {computed, reactive, ref, watch} from "vue";
import {currentSemester, currentSemesterName, getSubByTime, subSemester} from "./semester";
import {occupyColor, unOccupyColor} from "../color";


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

export const selections = computed(() => {
    if (subSemester.value !== 'full')
        return Object.assign({}, _selections[subSemester.value], _selections.full)
    return _selections.full
})
export const currentSelections = computed(() => {
    const ret = {}
    Object.keys(selections.value).forEach((courseName) => {
        const courseInfo = Object.assign({}, currentSemester.value.courses[courseName])
        const temp = {}
        selections.value[courseName].forEach(crn => {
            temp[crn] = courseInfo.sections[crn]
        })
        courseInfo.sections = selections.value[courseName].length
            ? temp
            : undefined
        ret[courseName] = courseInfo
    })
    return ret
})

export const displayedSelections = computed(() =>
    Object.assign({}, _selections.first, _selections.second, _selections.full)
)

export const toggleCourse = (courseInfo, value) => {
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