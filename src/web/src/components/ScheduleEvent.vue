<template functional>
  <div class="schedule-event" :style="data.style" data-cy="schedule-event">
    <div class="event-text">
      <span data-cy="title">
        <a v-bind:href="$options.getExploreCourseLink(props.name)">
          {{ props.title }}
        </a>
      </span>
      <br />
      <span data-cy="name">{{ props.name }}</span>
      &nbsp;-&nbsp;
      <span data-cy="section">{{ props.section }}</span>
      <br />
      <span data-cy="session_type">{{ props.session_type }}</span>
      <br />
      <span data-cy="instructor">{{ props.instructor }}</span>
      <br />
      <span data-cy="location">{{ props.location }}</span>
      <br />
      <span data-cy="crn">{{ props.crn }}</span>
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
    font-size: 60%;
    box-sizing: border-box;
    height: 100%;
    overflow-y: auto;
    // CSS Standard Scrollbar Control
    scrollbar-width: thin;

    //Changes the link color to black
    a {
      color: #000000;
    }
  }

  // WebKit Based Scrollbar Control
  .event-text::-webkit-scrollbar {
    width: 0.6em;
    height: 0.6em;
  }
  .event-text::-webkit-scrollbar-track {
    background-color: transparent;
  }
  .event-text::-webkit-scrollbar-thumb {
    background-color: rgba(128, 128, 128, 0.7);
    border-radius: 1.8em;
    border: transparent;
  }
  .event-text::-webkit-scrollbar-corner {
    background-color: transparent;
  }
}
</style>
