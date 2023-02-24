<template>
  <div class="search-bar">
    <input type="text" v-model="searchQuery" placeholder="Search...">
    <button @click="search">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    search() {
      // Perform search operation based on searchQuery
      console.log(`Searching for ${this.searchQuery}`);
    },
  },
};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  background-color: #f1f1f1;
}

input[type="text"] {
  padding: 5px;
  margin-right: 5px;
  border: none;
  border-radius: 3px;
  font-size: 16px;
}

button {
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  background-color: #4CAF50;
  color: white;
  font-size: 16px;
  cursor: pointer;
}
</style>