<template>
  <div
    class="schedule-event"
    data-cy="schedule-event"
    tabindex="-1"
    :style="data.style"
    :id="props.crn + props.day + props.startTime"
  >
    <div class="event-text">
      <span data-cy="title">{{ props.title }}</span>
      <br />
      <span data-cy="section">Section: {{ props.section }}</span>
      <br />
      <span data-cy="time">{{ props.time }}</span>
      <br />
      <span data-cy="location">{{ props.location }}</span>
      <br />
    </div>
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
  position: absolute;
  //height: 20%;
  //   width: 20%;

  //margin-top: 1px;
  border-left: 4px solid;
  //   border-opacity: 1;
  overflow: hidden;
  height: 100%;
  cursor: pointer;
  pointer-events: auto;

  .event-text {
    padding: 4px;
    font-weight: bold;
    font-size: 65%;
    box-sizing: border-box;
    height: 100%;
    overflow: hidden;
    // // CSS Standard Scrollbar Control
    // scrollbar-width: thin;

    // Changes the title color to black
    span[data-cy="title"] {
      color: #000;
      font-size: 105%;
    }
  }
}
</style>
