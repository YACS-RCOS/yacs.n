<template>
  <div>
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
  body {
    overflow-x: hidden;
  }
</style>
