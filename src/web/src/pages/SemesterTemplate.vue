<template>
<div>
    <div>
        <input class="text-input" v-model="textInput" type="text" placeholder="course name" @keyup.enter="courselist">
    </div>
    <div class="fulfilled-list">
        <li v-for="course in courses" :key="course">
            {{ course }}
        </li>
    </div>

    <div>
        <h1> Course Template </h1>
        
    </div>


</div>
</template>

<script>
export default {
    data() {
      return {
        courses: []

      };
    },
    methods: {
        async courselist(){
            let course = this.textInput;
            const response1 = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({course}),
            });

            this.courses = await response1.json();
        },
    },
};
</script>

<style scoped>
    .fulfilled-list{
        font-size: 1em;
    }
</style>

