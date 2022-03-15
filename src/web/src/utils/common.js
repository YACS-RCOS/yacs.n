export const filterCourses = (courses) => {
    return courses.filter((course) => {
        course.sections = course.sections && course.sections.filter(section => !!section)
        return course.sections && course.sections.length
    })
}

/**
 * Formats a `Date` into postgres date format
 * @param {Date} date
 * @returns {string} string in the format `YYYY-MM-DD`
 */
 export const standardDate = (date) => {
    let day = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate();
    let month =
      date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1;
    let year = date.getFullYear();
    return `${year}-${month}-${day}`;
  };