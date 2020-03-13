import moment from 'moment';
/**
 * Formats a `Date` into a readable format
 * @param {Date} date 
 * @returns {string} string in the format `M/D` where `M` is the 
 * month digit starting from 1 and `D` is day digit
 */
export const readableDate = (date) => {
    return `${date.getMonth() + 1}/${date.getDate()}`;
}
/**
 * Formats a time string into a readable format
 * @param {string} timeString in the format `kk:mm:ss` where `kk` is hours 1 to 24
 * @returns {string} string in the format `h:mma` where `a` is `'am'` or `'pm'`
 */
export const readableTime = (timeString) => {
    return moment(timeString, 'kk:mm:ss').format('h:mma');
}
/**
 * Migrated from old YACS  
 * Converts minutes into readable string
 * @param {number} minutes 
 * @returns {string} string with hour and am/pm
 */
export const hourName = (minutes) => {
    const hour = minutes / 60;
    if (hour === 0) {
        return '12 AM';
    } else if (hour < 12) {
        return hour + ' AM';
    } else if (hour === 12) {
        return 'Noon';
    } else {
        return (hour - 12) + ' PM';
    }
}

/**
 * Converts a time string into number of minutes since midnight
 * @param {string} timeString in the format `kk:mm:ss` where `kk` is hours 1 to 24
 * @returns {number} minutes since midnight
 */
export const toMinutes = (timeString) => {
    const mmt = moment(timeString, 'kk:mm:ss');
    return mmt.hours() * 60 + mmt.minutes();
}