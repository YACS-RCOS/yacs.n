<template>
  <div class="schedule-event">
    <div class="event-text">
      <!-- {{ period.section.listing.subjectShortname }} {{ period.section.listing.courseShortname }} - {{ period.section.shortname }}<br> -->
      {{ crn }} -
      <!-- {{ semester }} <br> -->
      {{ section }}
      <br />
      <!-- {{ period.section.instructors.join(', ') }}<br> -->
      <!-- {{ period.location }} -->
    </div>
  </div>
</template>

<script>
/**
 * @module ScheduleEventComponent
 * Renders a single schedule block
 * Dimensions and color of the block are done by the parent component
 * through inline styles
 */
export default {
  name: 'ScheduleEvent',
  props: {
    crn: String,
    semester: String,
    section: String
  }
};
</script>

<style lang="scss">
.schedule-event {
  display: block;
  box-sizing: border-box;
  border-top: 1px solid #e7e7e7 !important; //temp fix for the borders not showing
  border-right: 1px solid #e7e7e7 !important;
  position: absolute;
  //height: 20%;
  //   width: 20%;

  //margin-top: 1px;
  border-left: 4px solid;
  //   border-opacity: 1;
  overflow: hidden;
  height: 100%;

  .event-text {
    padding: 4px;
    font-weight: bold;
    font-size: small;
    box-sizing: border-box;
  }
}
</style>
