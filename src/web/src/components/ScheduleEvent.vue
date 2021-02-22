<template functional>
  <div class="schedule-event" :style="data.style" data-cy="schedule-event">
    <div class="event-text">
      <span data-cy="title"> <a v-bind:href= "'/explore/' + props.name.split(' ')[0] + '/' + props.name.split(' ')[0] + '-' + props.name.split(' ')[1]"> {{props.title}}</a> </span>
      <br />
      <span data-cy="name">{{ props.name }}</span>
      &nbsp;-&nbsp;
      <span data-cy="section">{{ props.section }}</span>
      <br />
      <span data-cy="crn">{{ props.crn }}</span>
      <br />
      <!-- location placeholder -->
      <br />
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
    overflow-y: auto;
  }
}
</style>
