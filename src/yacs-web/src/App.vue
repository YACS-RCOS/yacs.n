<template>
  <div id="root">
    <Header></Header>
    <MainPage/>
  </div>
</template>

<script>
import MainPage from './pages/Main';

import Header from './components/Header';

export default {
  name: 'App',
  components: {
    MainPage,
    Header
  }
}
</script>

<style lang="scss">
#root, html, body {
  height:100%;
}
</style>
