/**
 * @typedef {import('@/index').Course} Course
 * @typedef {import('@/index').CourseSession} CourseSession
 * @typedef {import('@/index').Subsemester} Subsemester
 */
import ColorService from '@/services/ColorService';

/**
 * @module NotificationsMixin
 * Allows components to create various toast notifications
 * I'm thinking should probably move this to a plugin
 */
export default {
  methods: {
    /**
     * Generates a Bootstrap Toast notification of a schedule conflict
     * using the provided information
     * @param {Course} course
     * @param {CourseSession} conflictSession
     * @param {Subsemester} subsemester
     */
    notifyScheduleConflict(course, conflictSession, subsemester) {
      const vNodesMsg = this.$createElement('p', { class: ['mb-0'] }, [
        `${subsemester.display_string}: Conflict with ${conflictSession.crn} - ${conflictSession.section} `,
        this.$createElement('div', {
          style: `
            background-color:${ColorService.getBackgroundColor(conflictSession)};
            border:1px solid ${ColorService.getBorderColor(conflictSession)};
            width:13px;
            height:13px;
            display:inline-block;`
        })
      ]);
      this.$bvToast.toast(vNodesMsg, {
        // title: `Cannot add ${section.crn} - ${section.sessions[0].section}`,
        title: `Cannot add ${course.title}`,
        variant: 'danger',
        noAutoHide: true
      });
    }
  }
};
