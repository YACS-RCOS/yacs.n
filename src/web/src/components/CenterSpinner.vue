<template>
  <div id="spinner" :style="renderStyle">
    <b-spinner></b-spinner>
    <div class="m-2">Loading {{loadingMessage}}...</div>
  </div>
</template>

<script>
export default {
  name: 'CenterSpinner',
  props: {
    height: Number,
    fontSize: Number,
    loadingMessage: String,
    topSpacing: Number,
  },
  computed: {
    renderStyle() {
      return "padding-top: " + this.topSpacing + "vh;" + 
             "font-size: " + this.fontSize + "em;" +
             "height: " + this.height + "vh;" +
             "text-align: center;";
    }
  },
  async created() {
    console.log("TOP PADDING " + this.topSpacing + '\n' + 
                "FONT SIZE " + this.fontSize + '\n' + 
                "LOADING MESSAGE " + this.loadingMessage + "\n" +
                "HEIGHT " + this.height + "\n"
    );
  }
}
</script>