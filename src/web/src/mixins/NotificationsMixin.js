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
     * Generates a Bootstrap Toast notification of a schedule conflict
     * using the provided information
     * @param {Course} course
     * @param {CourseSession} conflictSession
     * @param {Subsemester} subsemester
     */
    notifyScheduleConflict(course, existSession, addSession) {
      //NOTE: If Sub-Semester Data Desired, Need To Add As Parameter + 
      //Pass From CourseScheduler.vue. 
      // const vNodesMsg = this.$createElement("p", { class: ["mb-0"] }, [
      //   `${subsemester.display_string}: Conflict With ${existSession.crn}
      //         - ${existSession.section} `,
      const vNodesMsg = this.$createElement("p", { class: ["mb-0"] }, [
        `${existSession.crn} Conflicts With ${addSession.crn} 
          At ${addSession.time_start} `,
        this.$createElement("div", {
          style: `
            background-color:${getBackgroundColor(existSession)};
            border:1px solid ${getBorderColor(existSession)};
            width:13px;
            height:13px;
            display:inline-block;`,
        }),
      ]);
      this.$bvToast.toast(vNodesMsg, {
        // title: `Cannot add ${section.crn} - ${section.sessions[0].section}`,
        title: `Cannot Add ${course.title} [${addSession.crn}]`,
        variant: "danger",
        noAutoHide: false,
      });
    },
  },
};
