/**
 * A collection of handy functions
 * @module utils
 */

import moment from 'moment';

/** Short names of days of the week starting Sunday e.g. `DAY_SHORTNAMES[0]` is `'Sun'` */
export const DAY_SHORTNAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
/** Long names of days of the week starting Sunday e.g. `DAY_LONGNAMES[0]` is `'Sunday'` */
export const DAY_LONGNAMES = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday'
];

/**
 * Formats a `Date` into a readable format
 * @param {Date} date
 * @returns {string} string in the format `M/D` where `M` is the
 * month digit starting from 1 and `D` is day digit
 */
export const readableDate = date => {
  return `${date.getMonth() + 1}/${date.getDate()}`;
};

/**
 * Formats a `Date` into postgres date format
 * @param {Date} date
 * @returns {string} string in the format `YYYY-MM-DD`
 */
export const standardDate = date => {
  let day = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate();
  let month = date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1;
  let year = date.getFullYear();
  return `${year}-${month}-${day}`;
};

/**
 * When retrieving dates from Postgres date type, it will be in GMT/UTC with a time of midnight.
 * This function attempts to preserve the original date specified in Postgres.
 * @param {Date} date
 * @returns {Date} date that has been offset from local timezone to UTC timezone
 */
export const localToUTCDate = date => {
  // JS dates will auto convert your passed in date string to
  // the local timezone. So, when the server gives back semester end date of Aug 21st 00:00:00 GMT,
  // in EST it becomes Aug 20th 20:00:00, where the timezone difference between EST and UTC is 4 hours.
  // Could either change the date type in the course table to timezone and set its time to midnight,
  // or this, which is offset the auto-converted local datetime by the 4 hours.
  date.setUTCHours(date.getUTCHours() + date.getTimezoneOffset()/60);
  return date;
}

/**
 * Formats a time string into a readable format
 * @param {string} timeString in the format `kk:mm:ss` where `kk` is hours 1 to 24
 * @returns {string} string in the format `h:mma` where `a` is `'am'` or `'pm'`
 */
export const readableTime = timeString => {
  return moment(timeString, 'kk:mm:ss').format('h:mma');
};

/**
 * Migrated from old YACS
 * Converts minutes into readable string
 * @param {number} minutes
 * @returns {string} string with hour and am/pm
 */
export const hourName = minutes => {
  const hour = minutes / 60;
  if (hour === 0) {
    return '12 AM';
  } else if (hour < 12) {
    return hour + ' AM';
  } else if (hour === 12) {
    return 'Noon';
  } else {
    return hour - 12 + ' PM';
  }
};

/**
 * Converts a time string into number of minutes since midnight
 * @param {string} timeString in the format `kk:mm:ss` where `kk` is hours 1 to 24
 * @returns {number} minutes since midnight
 */
export const toMinutes = timeString => {
  const mmt = moment(timeString, 'kk:mm:ss');
  return mmt.hours() * 60 + mmt.minutes();
};

// TODO make better
export function partition (arr, cmpFunc = null) {
  if (arr.length) {
    let pkgs = cmpFunc ? arr.sort(cmpFunc) : arr.sort();
    if (pkgs.length) {
        let groups = []
        let group = [pkgs[0]]
        for (let i = 1; i < pkgs.length; i++) {
            var pkg = pkgs[i];
            if (cmpFunc(pkg, group[0]) == 0) {
                group.push(pkg)
            }
            else {
                groups.push(group)
                group = [pkg]
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