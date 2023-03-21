<script>
export default {
    name:"Prerequisites",
    data() {
    return {
      Prerequisites: 'Select your classes from the menu below'
    }
  }
};
</script>

<template>
    <p class = "Prerequisites">{{ Prerequisites }}</p>
    
</template>

<style>
.Prerequisites{
    color: blue;
  font-weight: bold;
}

</style>