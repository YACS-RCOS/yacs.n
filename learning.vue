<template>
    <h1 :class="titleClass">{{welcome}}</h1>
    <h3 :class="subtitleClass">{{required}}</h3>
    <div v-for = "course in courses" :key="course.id">
        <input type = "checkbox" :id = "course.id" v-model = "course.checked" >
        <span :class="{ checked: course.checked }">{{ course.name }}</span>
    </div>
</template>

<script>
let id = 0
export default {
    data() {
        return{
            welcome: 'Welcome to YACS!',
            required: 'Required CS courses:',
            titleClass: 'title',
            subtitleClass: 'subtitle',
            courses: [
                {id: id++, name: 'Computer Science 1', checked: false},
                {id: id++, name: 'Data Structures', checked: false},
                {id: id++, name: 'Foundations of Computer Science', checked: false},
                {id: id++, name: 'Computer Organization', checked: false},
                {id: id++, name: 'Principles of Software', checked: false}
            ]
        }
    }
}
</script>

<style>
.title {
    color: rgb(167,255,255);
}
.subtitle {
    color: navy;
}
.checked {
    text-decoration: line-through;
}
</style>