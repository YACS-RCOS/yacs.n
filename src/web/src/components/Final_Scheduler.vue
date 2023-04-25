<template>
    <div class="calendar-container">
      <table>
        <thead>
          <tr>
            <th v-for="day in daysOfWeek">{{ day }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(week, index) in weeks" :key="index">
            <td v-for="(day, index) in week" :key="index" :class="{ event: isEvent(day), [getEventClass(day)]: isEvent(day) }">{{ day }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
<script>
export default {
data() {
    return {
    daysOfWeek: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    weeks: [],
    events: [
        { date: 1, title: 'Intro to Computer Science' },
        { date: 2, title: 'Data Structure' },
        { date: 3, title: 'Foundation to Computer Science' },
        { date: 4, title: 'Computer Organization' },
        { date: 5, title: 'Intro to Algorithm' }
    ]
    }
},
mounted() {
    this.buildCalendar()
},
methods: {
    buildCalendar() {
    const date = new Date(2023, 4, 1)
    const firstDayOfMonth = new Date(date.getFullYear(), date.getMonth(), 1)
    const lastDayOfMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0)
    const daysInMonth = lastDayOfMonth.getDate()
    const firstDayOfWeek = firstDayOfMonth.getDay()
    const weeks = []

    let week = []
    for (let i = 0; i < firstDayOfWeek; i++) {
        week.push('')
    }

    for (let i = 1; i <= daysInMonth; i++) {
        week.push(i)
        if (week.length === 7) {
        weeks.push(week)
        week = []
        }
    }

    if (week.length > 0) {
        for (let i = week.length; i < 7; i++) {
        week.push('')
        }
        weeks.push(week)
    }

    this.weeks = weeks
    },
    isEvent(day) {
    return this.events.some(event => event.date === day)
    },
    getEventClass(day) {
    const event = this.events.find(event => event.date === day)
    return event ? event.title.toLowerCase().replace(' ', '-') : ''
    }
}
}
</script>
  
<style>
.calendar-container {
float: right;
width: 70%;
}

table {
border-collapse: collapse;
}

th, td {
border: 1px solid black;
padding: 5px;
}

.event {
background-color: yellow;
}

</style>
  