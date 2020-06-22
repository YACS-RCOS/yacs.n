/**
 * A collection of handy functions
 * @module utils
 */

import moment from "moment";

/** Short names of days of the week starting Sunday e.g. `DAY_SHORTNAMES[0]` is `'Sun'` */
export const DAY_SHORTNAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
/** Long names of days of the week starting Sunday e.g. `DAY_LONGNAMES[0]` is `'Sunday'` */
export const DAY_LONGNAMES = [
  "Sunday",
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
];

export const ICS_DAY_SHORTNAMES = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"];

/**
 * Formats a `Date` into a readable format
 * @param {Date} date
 * @returns {string} string in the format `M/D` where `M` is the
 * month digit starting from 1 and `D` is day digit
 */
export const readableDate = (date) => {
  return `${date.getMonth() + 1}/${date.getDate()}`;
};

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
 * Formats a time string into a readable format
 * @param {string} timeString in the format `kk:mm:ss` where `kk` is hours 1 to 24
 * @returns {string} string in the format `h:mma` where `a` is `'am'` or `'pm'`
 */
export const readableTime = (timeString) => {
  return moment(timeString, "kk:mm:ss").format("h:mma");
};

/**
 * Migrated from old YACS
 * Converts minutes into readable string
 * @param {number} minutes
 * @returns {string} string with hour and am/pm
 */
export const hourName = (minutes) => {
  const hour = minutes / 60;
  if (hour === 0) {
    return "12 AM";
  } else if (hour < 12) {
    return hour + " AM";
  } else if (hour === 12) {
    return "Noon";
  } else {
    return hour - 12 + " PM";
  }
};

/**
 * Converts a time string into number of minutes since midnight
 * @param {string} timeString in the format `kk:mm:ss` where `kk` is hours 1 to 24
 * @returns {number} minutes since midnight
 */
export const toMinutes = (timeString) => {
  const mmt = moment(timeString, "kk:mm:ss");
  return mmt.hours() * 60 + mmt.minutes();
};

// TODO make better
export function partition(arr, cmpFunc = null) {
  if (arr.length) {
    let pkgs = cmpFunc ? arr.sort(cmpFunc) : arr.sort();
    if (pkgs.length) {
      let groups = [];
      let group = [pkgs[0]];
      for (let i = 1; i < pkgs.length; i++) {
        var pkg = pkgs[i];
        if (cmpFunc(pkg, group[0]) == 0) {
          group.push(pkg);
        } else {
          groups.push(group);
          group = [pkg];
        }
      }
      if (group.length) {
        groups.push(group);
      }
      return groups;
    }
    return pkgs;
  }
  return arr;
}

export const getClosestDay = (fromDay, sessions) => {
  if (sessions.length) {
    sessions.sort((session1, session2) => {
      // In DB, days are numbered MON 0 - FRI 4
      // In JS, days are numbered SUN 0 - SAT 6
      // Course start date will be on a week day, JS Date, Mon 1 - Fri 5
      // Shift the JS date range back by 1
      if (
        Math.abs(fromDay - 1 - session1.day_of_week) <
        Math.abs(fromDay - 1 - session2.day_of_week)
      ) {
        return -1;
      } else if (
        Math.abs(fromDay - 1 - session1.day_of_week) >
        Math.abs(fromDay - 1 - session2.day_of_week)
      ) {
        return 1;
      }
      return 0;
    });
    return sessions[0].day_of_week;
  }
  return -1;
};

/**
 * Checks whether `s1` spans the entire duration of `s2`
 * @param {Subsemester} s1
 * @param {Subsemester} s2
 * @returns {boolean}
 */
export const withinDuration = (s1, s2) => {
  return (
    s1.date_start.getTime() <= s2.date_start.getTime() &&
    s1.date_end.getTime() >= s2.date_end.getTime()
  );
};

export const generateRequirementsText = (prereqs, coreqs, raw) => {
  let text = [];
  if (prereqs || coreqs) {
    const same = JSON.stringify(prereqs) == JSON.stringify(coreqs);

    text.push("Requires");

    if (prereqs) {
      text.push("completion of");

      if (!same) text.push(prereqs.join(", "));
    }

    if (prereqs && coreqs) text.push(same ? "or" : "and");

    if (coreqs) {
      text.push("concurrent enrollment in");

      text.push(coreqs.join(", "));
    }
  } else {
    text.push("Requirements:", raw);
  }

  return text.join(" ");
};

export const compareSessionsByDate = (session1, session2) => {
  let d1_s = new Date(`Sat Apr 25 2020 ${session1.time_start}`);
  let d2_s = new Date(`Sat Apr 25 2020 ${session2.time_start}`);
  let d1_e = new Date(`Sat Apr 25 2020 ${session1.time_end}`);
  let d2_e = new Date(`Sat Apr 25 2020 ${session2.time_end}`);
  if (d1_s.getTime() === d2_s.getTime() && d1_e.getTime() === d2_e.getTime()) {
    return 0;
  } else if (d1_s < d2_s) {
    return -1;
  }
  return 1;
};

export const addDays = (date, days) => {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
};

/**
 * Export all selected course sections to ICS
 */
export const exportScheduleToIcs = (selectedCourses) => {
  let calendarBuilder = window.ics();
  let semester;
  for (const course of selectedCourses) {
    for (const section of course.sections.filter((s) => s.selected)) {
      const sessionsPartitionedByStartAndEnd = partition(
        section.sessions,
        compareSessionsByDate
      );
      for (const sessionGroupOfSameMeetTime of sessionsPartitionedByStartAndEnd) {
        const days = sessionGroupOfSameMeetTime.map(
          (sess) => ICS_DAY_SHORTNAMES[sess.day_of_week]
        );
        // Gets closest day to the course start date
        const firstDay = getClosestDay(
          course.date_start.getDay(),
          sessionGroupOfSameMeetTime
        );
        const session = sessionGroupOfSameMeetTime[0];
        // The dates from the DB have no timezone, so when they are
        // cast to a JS date they're by default at time midnight 00:00:00.
        // This will exclude all classes if they're on that final day, so bump
        // the end date by 1 day.
        let exclusive_date_end = new Date(course.date_end);
        exclusive_date_end.setDate(course.date_end.getDate() + 1);
        // Moment numbers days from 0 SUN - 6 MON - 7 NEXT SUNDAY
        // firstDay is numbered     0 MON - 4 FRI, so need to add 1 to match moment's spec
        let dtStart = moment(course.date_start)
          .day(firstDay + 1)
          .toDate();
        if (dtStart < course.date_start) {
          // Go to NEXT week, uses the current week by default
          dtStart = moment(course.date_start)
            .day(firstDay + 1 + 7)
            .toDate();
        }
        semester = section.semester;
        // https://github.com/nwcell/ics.js/blob/master/ics.js#L50
        calendarBuilder.addEvent(
          `${course.full_title || course.title}`,
          `${course.department}-${course.level} ${session.section}, CRN: ${session.crn}  [from YACS]`, // Add professor and type of class (LEC || LAB) to this description arg when data is available
          "", // session.location,
          new Date(`${dtStart.toDateString()} ${session.time_start}`),
          new Date(`${dtStart.toDateString()} ${session.time_end}`),
          {
            freq: "WEEKLY",
            interval: 1,
            until: exclusive_date_end,
            byday: days,
          }
        );
      }
    }
  }
  calendarBuilder.download(
    `${semester.replace(/^(\w)(\w*?)\s?(\d+)/, function (
      _,
      semFirstLetter,
      semRest,
      year
    ) {
      return semFirstLetter.toUpperCase() + semRest.toLowerCase() + year;
    })}_Schedule`
  );
};
