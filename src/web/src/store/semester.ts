import {
  computed,
  ComputedRef,
  effect,
  reactive,
  watch,
  watchEffect
} from 'vue'
import {
  getCourses,
  getDefaultSemester,
  getSemester
} from '../plugins/axios/api'
import yacs from './local'

;(function () {
  !yacs.currentSemester &&
    getDefaultSemester().then((res: any) => (yacs.currentSemester = res))
})()

const parseSession = (sessions: any[]): number[] => {
  try {
    return sessions.reduce(
      (arr, session) => {
        const a = session['time_start']
          .split(':')
          .map((x: string) => Number.parseInt(x))
        const b = session['time_end']
          .split(':')
          .map((y: string) => Number.parseInt(y))
        const duration = Math.abs(
          (b[0] - a[0]) * 2 + (a[1] < 30 ? 1 : 0) + (b[1] >= 30 ? 1 : 0)
        )
        const end = (20 - b[0]) * 2 + (b[1] < 30 ? 1 : 0)
        arr[session['day_of_week']] |= ((1 << duration) - 1) << end
        return arr
      },
      [0, 0, 0, 0, 0]
    )
  } catch (e) {
    // console.warn('session missing essential attributes!')
    return [0, 0, 0, 0, 0]
  }
}

const temp = computed(() => {
  const dict = new Map()
  getCourses(yacs.currentSemester).then((data) => {})
})

const dictionary: Map<string, { sections: Map<string, any> }> = reactive(
  new Map()
)
watchEffect(() => {
  getCourses(yacs.currentSemester).then((data) => {
    data.forEach((course: any) => {
      const newSections = new Map()
      course.sections.forEach((section: any) => {
        if (!section) return
        section.times = parseSession(section.sessions)
        newSections.set(section.crn, section)
      })
      course.sections = newSections
      dictionary.set(course.title, course)
    })
  })
})

const selectionInfo = computed(() => {
  const m: Map<any, any[]> = new Map()
  if (!dictionary.size) return m
  Object.keys(yacs.courseSelection).forEach((title: string) => {
    const c = dictionary.get(title)
    const arr = yacs.courseSelection[title].map((crn) => c!.sections.get(crn))
    m.set(c, arr)
  })
  return m
})

Object.assign(yacs.courseSelection, { 'DATA STRUCTURES': ['60371'] })

const defaultCourses = ['DATA STRUCTURES']

const courseList = computed(() =>
  defaultCourses
    .filter((title) => dictionary.has(title))
    .map((title) => dictionary.get(title))
)

// console.log(courseList.value)

interface Possibility {
  info: Record<string, any>
  times: number[]
}

const generateSchedules = () => {
  let newPossibilities: Possibility[] = [
    {
      info: {},
      times: [0, 0, 0, 0, 0]
    }
  ]
  let ret: Possibility[] = []
  for (let [course, sections] of selectionInfo.value) {
    try {
      newPossibilities.forEach((possibility: Possibility) => {
        ret = ret.concat(addCourse(course.full_title, sections, possibility))
      })
    } catch (e) {
      console.log(`cannot add course ${course.full_title}`)
    }
  }
  return ret
}

const addCourse = (title: string, sections: any[], schedule: Possibility) => {
  const ret: Possibility[] = []
  sections.forEach((section: any) => {
    const newSection = addSection(title, section, schedule)
    newSection && ret.push(newSection)
  })
  if (!ret.length) {
    throw new Error(`conflict`)
  }
  return ret
}

const addSection = (title: string, section: any, schedule: Possibility) => {
  const newSchedule: Possibility = JSON.parse(JSON.stringify(schedule))
  for (let i = 0; i < 5; i++) {
    if ((section.times[i] & schedule.times[i]) > 0) {
      return null
    }
    newSchedule.times[i] |= section.times[i]
  }
  newSchedule.info[title] = section
  return newSchedule
}

const possibilities = computed(() => {
  return generateSchedules()
})

export { courseList, selectionInfo }
