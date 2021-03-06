import "@/typedef";

import { getBackgroundColor, getBorderColor } from "@/services/ColorService";

import moment from "moment";
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
     * @param {Course} conflictCourse = Existing Conflict Course,
     * @param {CourseSession} addSession = Course Session Data For Attempted Course.
     * @param {CourseSession} existSession = Course Session Data For Existing Course.
     */
    notifyScheduleConflict(
      addCourse,
      conflictCourse,
      addSession,
      existSession
    ) {
      const formatStartTime = moment(existSession.time_start, ["HH.mm"]).format(
        "hh:mm A"
      );
      //Format All Message Data For Conflict Message:
      const vNodesMsg = this.$createElement("p", { class: ["mb-0"] }, [
        `${addCourse.title} [${addSession.crn}] 
          Conflicts With ${conflictCourse.title} [${existSession.crn}]
          At ${formatStartTime} `,
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
        title: `Cannot Add ${addCourse.title}`,
        variant: "danger",
        noAutoHide: false,
      });
    },
    notifyCreditConflict(){
      //Format All Message Data For Conflict Message:
      const vNodesMsg = this.$createElement("p", { class: ["mb-0"] }, [
        'WARNING: Exceeding Credits Limit'
        ]);
      //Format All Header-Data For Conflict Message:
      this.$bvToast.toast(vNodesMsg, {
        title: `CREDIT CAP`,
        variant: "danger",
        noAutoHide: false,
      });
    },
  },
};
