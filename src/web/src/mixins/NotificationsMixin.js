import "@/typedef";

import { getBackgroundColor, getBorderColor } from "@/services/ColorService";

/**
 * Allows components to create various toast notifications
 * I'm thinking should probably move this to a plugin
 * @module NotificationsMixin
 */
export default {
  methods: {
    /**
     * Generates a Bootstrap Toast Notification of a Schedule Conflict
     * Using The Provided Information, Specified Below:
     * @param {Course} addCourse = Course Tried To Add,
     * @param {Course} existCourse = Existing Conflict Course,
     * @param {CourseSession} addSession = Course Session Data For Attemped Course.
     * @param {CourseSession} existSession = Course Session Data For Existing Course.
     */
    notifyScheduleConflict(addCourse, existCourse, addSession, existSession) {
      //NOTE: If Sub-Semester Data Desired, Need To Add As Parameter +
      //Pass From CourseScheduler.vue.
      // const vNodesMsg = this.$createElement("p", { class: ["mb-0"] }, [
      //   `${subsemester.display_string}: Conflict With ${existSession.crn}
      //         - ${existSession.section} `,
      const vNodesMsg = this.$createElement("p", { class: ["mb-0"] }, [
        `${addCourse.title} [${addSession.crn}] 
          Conflicts With ${existCourse.title} [${existSession.crn}]
          At ${existSession.time_start} `,
        this.$createElement("div", {
          style: `
            background-color:${getBackgroundColor(existSession)};
            border:1px solid ${getBorderColor(existSession)};
            width:13px;
            height:13px;
            display:inline-block;`,
        }),
      ]);
      //Format All Header-Data For Conflict Message:
      this.$bvToast.toast(vNodesMsg, {
        // title: `Cannot add ${section.crn} - ${section.sessions[0].section}`,
        title: `Failure: Cannot Add ${addCourse.title} [${addSession.crn}]`,
        variant: "danger",
        noAutoHide: false,
      });
    },
  },
};
