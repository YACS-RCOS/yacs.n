<template>
  <b-spinner></b-spinner>
  <div class="m-2">Loading {{loadingMessage}}...</div>
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
  }
}
</script>