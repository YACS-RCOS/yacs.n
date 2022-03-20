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

/**
 * When retrieving dates from Postgres date type, it will be in GMT/UTC with a time of midnight.
 * This function attempts to preserve the original date specified in Postgres.
 * @param {Date} date
 * @returns {Date} date that has been offset from local timezone to UTC timezone
 */
 export const localToUTCDate = (date) => {
  // JS dates will auto convert your passed in date string to
  // the local timezone. So, when the server gives back semester end date of Aug 21st 00:00:00 GMT,
  // in EST it becomes Aug 20th 20:00:00, where the timezone difference between EST and UTC is 4 hours.
  // Could either change the date type in the course table to timezone and set its time to midnight,
  // or this, which is offset the auto-converted local datetime by the 4 hours.
  date.setUTCHours(date.getUTCHours() + date.getTimezoneOffset() / 60);
  return date;
};

/**
 * Formats a `Date` into a readable format
 * @param {Date} date
 * @returns {string} string in the format `M/D` where `M` is the
 * month digit starting from 1 and `D` is day digit
 */
 export const readableDate = (date) => {
  return `${date.getMonth() + 1}/${date.getDate()}`;
};
