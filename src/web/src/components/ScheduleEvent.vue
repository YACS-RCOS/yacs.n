<template functional>
  <div class="schedule-event" :style="data.style">
    <div class="event-text">
      {{ props.title }}
      <br>
      {{ props.name }} - {{ props.section }}
      <br>
      {{ props.crn }}
      <br>
      <!-- location placeholder -->
      <br>
      <!-- professor placeholder -->
    </div>
  </div>
</template>
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
    y-overflow: auto;
  }
}
</style>
