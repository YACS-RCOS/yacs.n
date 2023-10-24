/**
 * A collection of handy functions
 * @module utils
 */

import moment from "moment";
import domtoimage from "dom-to-image";

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
  if (!prereqs && !coreqs && !raw) {
    return "This course has no prerequisites";
  }
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
 * Export Course Data Given Course Session CRN Value.
 */
export const findCourseByCourseSessionCRN = (allCourseData, inputCRNValue) => {
  return allCourseData.find((currentCourse) => {
    //Search For Desired CRN In Current Course.
    let isFound = currentCourse.sections.some((currentSection) => {
      return currentSection.crn === inputCRNValue;
    });
    //Found Course w/ Appropriate CRN.
    if (isFound) {
      return currentCourse;
    }
  });
};

/**
 * Export all selected course sections to ICS
 */
export const exportScheduleToIcs = (selectedSections) => {
  let calendarBuilder = window.ics();
  let semester;
  // Handle Special Case Where No Selected Courses On Schedule.
  if (selectedSections[0].length == 0) {
    alert("No Courses Found For Export To ICS Data.");
    return;
  }
  for (const section of selectedSections[0]) {
    const sessionsPartitionedByStartAndEnd = partition(
      section.sessions,
      compareSessionsByDate
    );
    for (const sessionGroupOfSameMeetTime of sessionsPartitionedByStartAndEnd) {
      const days = sessionGroupOfSameMeetTime.map(
        (sess) => ICS_DAY_SHORTNAMES[sess.day_of_week]
      );
      const date_start = localToUTCDate(new Date(section.date_start));
      const date_end = localToUTCDate(new Date(section.date_end));
      // Gets closest day to the course start date
      const firstDay = getClosestDay(
        date_start.getDay(),
        sessionGroupOfSameMeetTime
      );
      const session = sessionGroupOfSameMeetTime[0];
      // The dates from the DB have no timezone, so when they are
      // cast to a JS date they're by default at time midnight 00:00:00.
      // This will exclude all classes if they're on that final day, so bump
      // the end date by 1 day.
      let exclusive_date_end = new Date(date_end);
      exclusive_date_end.setDate(date_end.getDate() + 1);
      // Moment numbers days from 0 SUN - 6 MON - 7 NEXT SUNDAY
      // firstDay is numbered     0 MON - 4 FRI, so need to add 1 to match moment's spec
      let dtStart = moment(date_start)
        .day(firstDay + 1)
        .toDate();
      if (dtStart < date_start) {
        // Go to NEXT week, uses the current week by default
        dtStart = moment(date_start)
          .day(firstDay + 1 + 7)
          .toDate();
      }
      semester = section.semester;
      // https://github.com/nwcell/ics.js/blob/master/ics.js#L50
      calendarBuilder.addEvent(
        `${section.title}`,
        `${section.department}-${section.level} ${session.section}, CRN: ${session.crn}  [from YACS]`, // Add professor and type of class (LEC || LAB) to this description arg when data is available
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

/**
 * Export all selected final exam sections to ICS
 */
export const exportFinalToIcs = (selectedSections) => {
  if (!Array.isArray(selectedSections) || selectedSections[0] == null) {
    alert("No Final Exam Sections Found For Export to ICS.");
    return;
  }

  let calendarFinals = window.ics();
  let semester = "current";

  selectedSections.forEach((course) => {
    const startTime = course.Hour.split("-")[0].trim();
    const endTime = course.Hour.split("-")[1].trim();

    const examDate = new Date(course.Day);
    const startDate = new Date(examDate);

    let startHour = parseInt(startTime.split(":")[0]);
    let startMinute = parseInt(startTime.split(":")[1].substring(0, 2));

    startDate.setHours(startHour);
    startDate.setMinutes(startMinute);
    startDate.setFullYear(new Date().getFullYear());
    if (startTime.split(":")[1].substring(2) === "PM") {
      startDate.setHours(startDate.getHours() + 12);
    }

    const endDate = new Date(examDate);

    let endHour = parseInt(endTime.split(":")[0]);
    let endMinute = parseInt(endTime.split(":")[1].substring(0, 2));
    
    endDate.setHours(endHour);
    endDate.setMinutes(endMinute);
    endDate.setFullYear(new Date().getFullYear());
    if (endTime.split(":")[1].substring(2) === "PM") {
      endDate.setHours(endDate.getHours() + 12);
    }

    calendarFinals.addEvent(
      `${course.Department} ${course.CourseCode}-${course.Section}`,
      `${course.Department} Final Exam`,
      course.Room,
      startDate,
      endDate,
      {
        freq: "DAILY",
        interval: 1,
        until: endDate,
      }
    );
  });
  calendarFinals.download(`${semester.replace(/\s+/g, "_")}_Final_Exams`);
};



/**
 * Takes an object with the constant types for a vuex module and
 * the associated namespace, then adds the namespace prefix
 * to all definitions while adding a `local` property with the
 * original definitions.
 * ```
 * prefixNamespacedTypes("user", {
 *   actions: {
 *    LOGIN: "login",
 *    LOGOUT: "logout"
 *  }
 * })
 * // which will return
 * {
 *   actions: {
 *     LOGIN: "user/login",
 *     LOGOUT: "user/logout"
 *   },
 *   local: {
 *     actions: {
 *       LOGIN: "login",
 *       LOGOUT: "logout"
 *     }
 *   },
 *   namespace: "user"
 * }
 *
 * ```
 * @template M
 * @param {M} types
 * @param {string} namespace
 * @returns {M & {local: M; namespace: string}}
 */
export const prefixNamespacedTypes = (namespace, types) => {
  const namespacedTypes = {};

  Object.keys(types).forEach((block) => {
    namespacedTypes[block] = {};
    Object.keys(types[block]).forEach((key) => {
      namespacedTypes[block][key] = namespace + "/" + types[block][key];
    });
  });
  namespacedTypes.local = types;
  namespacedTypes.namespace = namespace;

  return namespacedTypes;
};

/*
 * Export The Course Schedule To An Image Format, Probably PNG.
 * Can Come Back Here + Add More File Format Options, Such As JPEG, ...
 * NOTE: In Case More Specifications Are Needed For Image, Modify Options
 * Attribute Passed In Via Scheduler.Vue.
 * Additionally, To Change The Scope For Image, Also View Schedule.Vue
 * + Look For ID = "allScheduleData" To See Scope Image.
 */
export const exportScheduleToImage = (
  selectedCourses,
  q,
  options
) => {
  // Handle Special Case Where No Selected Courses On Schedule.
  if (selectedCourses.length == 0) {
    alert("No Courses Found For Export To Image Data.");
    return;
  }
  // Obtain Schedule Element Defined In Schedule.Vue File + Run Export To PNG.
  domtoimage
    .toPng(document.getElementById("allScheduleData"), options)
    .then(function (dataUrl) {
      var link = document.createElement("a");
      link.download = currentSemester.replace(" ", "-") + "-YACS-Schedule.png";
      link.href = dataUrl;
      link.click();
    })
    .catch(function (error) {
      console.log("Oh No, Something Went Wrong!", error);
    });
};

export const exportFinaltoImage = (selectedSections) => {
  if (!Array.isArray(selectedSections) || selectedSections[0] == null) {
    alert("No Final Exam Sections Found For Export to Image Data.");
    return;
  }
  
}; 

export const getLongName = (department) => {
  var dict = {
    ARTS: "Arts",
    COGS: "Cognitive Science",
    STSH: "Science and Technology Studies - Humanities",
    STSS: "Science and Technology Studies - Social Sciences",
    COMM: "Communication",
    ECON: "Economics",
    GSAS: "Games and Simulations Arts and Sciences",
    IHSS: "Interdisciplinary H&SS",
    LANG: "Languages",
    LITR: "Literature",
    PHIL: "Philosophy",
    PSYC: "Psychology",
    WRIT: "Writing",
    BMED: "Biomedical Engineering",
    CHME: "Chemical Engineering",
    ECSE: "Electrical and Computer Systems Engineering",
    ENVE: "Environmental and Energy Engineering",
    MANE: "Mechanical, Aerospace, and Nuclear Engineering",
    MTLE: "Materials Science and Engineering",
    CIVL: "Civil Engineering",
    ENGR: "Core Engineering",
    ISYE: "Industrial and Systems Engineering",
    EPOW: "Electrical Power Engineering",
    BCBP: "Biochemistry and Biophysics",
    CSCI: "Computer Science",
    ERTH: "Earth and Environmental Science",
    IENV: "Interdisciplinary Environmental",
    ISCI: "Interdisciplinary Science",
    MATP: "Math Programming, Probability, and Statistics",
    PHYS: "Physics",
    ASTR: "Astronomy",
    BIOL: "Biology",
    CHEM: "Chemistry",
    MATH: "Mathematics",
    ITWS: "Information Technology and Web Science",
    ARCH: "Architecture",
    LGHT: "Lighting",
    MGMT: "Management",
    ADMN: "Adminstrative Courses",
    USAF: "Aerospace Studies (Air Force ROTC)",
    USNA: "Naval Science (Navy ROTC)",
    USAR: "Military Science (ARMY ROTC)",
  };

  return dict[department];
};
