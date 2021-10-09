<template functional>
  <div
    class="schedule-event"
    data-cy="schedule-event"
    tabindex="-1"
    :style="data.style"
    :id="props.crn + props.day + props.startTime"
  >
    <div class="event-text">
      <span data-cy="name">{{ props.name }}</span>
      &nbsp;–&nbsp;
      <span data-cy="section">{{ props.section }}</span>
      <br />
      <span data-cy="sessionType">{{ props.sessionType }}</span>
      <br />
      <span data-cy="location">{{ props.location }}</span>
      <br />
    </div>
    <b-popover
      :title="props.name + ' – ' + props.section"
      :target="props.crn + props.day + props.startTime"
      triggers="click blur"
      placement="top"
    >
      <h6 data-cy="title">
        <a v-bind:href="$options.getExploreCourseLink(props.name)">
          {{ props.title }}
        </a>
      </h6>
      <b>Session Type</b><br />
      <span data-cy="sessionType">{{ props.sessionType }}</span>
      <br />
      <b>Instructor</b><br/>
      <span data-cy="instructor">{{ props.instructor }}</span>
      <br />
      <b>Location</b><br />
      <span data-cy="location">{{ props.location }}</span>
      <br />
      <b>Session Time</b><br />
      <span data-cy="time">{{ props.startTime }}–{{ props.endTime }}</span>
      <br />
      <b>CRN</b><br />
      <span data-cy="crn">{{ props.crn }}</span>
      <br />
    </b-popover>
  </div>
</template>
<script>
export default {
  getExploreCourseLink(courseName) {
    var subject = courseName.split(" ")[0];
    var courseNumber = courseName.split(" ")[1];
    return `/explore/${subject}/${subject}-${courseNumber}`;
  },
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
  cursor: pointer;

  .event-text {
    padding: 4px;
    font-weight: bold;
    font-size: 65%;
    box-sizing: border-box;
    height: 100%;
    overflow: hidden;
    // // CSS Standard Scrollbar Control
    // scrollbar-width: thin;

    // //Changes the link color to black
    // a {
    //   color: #000000;
    // }
  }

  // // WebKit Based Scrollbar Control
  // .event-text::-webkit-scrollbar {
  //   width: 0.6em;
  //   height: 0.6em;
  // }
  // .event-text::-webkit-scrollbar-track {
  //   background-color: transparent;
  // }
  // .event-text::-webkit-scrollbar-thumb {
  //   background-color: rgba(128, 128, 128, 0.7);
  //   border-radius: 1.8em;
  //   border: transparent;
  // }
  // .event-text::-webkit-scrollbar-corner {
  //   background-color: transparent;
  // }
}
</style>
