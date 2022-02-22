export const filterCourses = (courses) => {
    return courses.filter((course) => {
        course.sections = course.sections && course.sections.filter(section => !!section)
        return course.sections && course.sections.length
    })
}