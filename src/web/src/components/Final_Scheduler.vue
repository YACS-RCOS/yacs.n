<template>
  <div class="calendar">
    <table>
      <thead>
        <tr>
          <th>Mon</th>
          <th>Tue</th>
          <th>Wed</th>
          <th>Thu</th>
          <th>Fri</th>
          <th>Sat</th>
          <th>Sun</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="week in weeks" :key="week">
          <td v-for="day in week" :key="day.date" :class="{'prev-month': day.prevMonth, 'next-month': day.nextMonth, 'today': day.today}">
            {{ day.date.getDate() }}
            <div v-for="event in eventsOnDay(day.date)" :key="event.title" class="event">{{ event.title }}</div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      daysInWeek: 7,
      weeks: [],
      events: [
        {
          date: new Date(2023, 4, 3),
          title: "Math exam"
        },
        {
          date: new Date(2023, 4, 8),
          title: "History essay due"
        },
        {
          date: new Date(2023, 4, 10),
          title: "Science lab report due"
        },
        {
          date: new Date(2023, 4, 16),
          title: "English presentation"
        },
        {
          date: new Date(2023, 4, 20),
          title: "Art project due"
        },
        {
          date: new Date(2023, 4, 25),
          title: "Physical education final exam"
        },
        {
          date: new Date(2023, 4, 28),
          title: "Music recital"
        }
      ]
    };
  },
  mounted() {
    this.generateCalendar();
  },
  methods: {
    generateCalendar() {
      const date = new Date();
      date.setFullYear(2023); // Set the year to 2023
      date.setMonth(4); // Set the month to May
      date.setDate(1); // Set the date to the 1st of the month

      const month = date.getMonth();
      const year = date.getFullYear();

      let dayOfWeek = date.getDay(); // Get the day of the week of the 1st

      // Add days from the previous month to fill the first week
      while (dayOfWeek > 0) {
        this.weeks.push({
          date: new Date(year, month, -dayOfWeek + 1),
          prevMonth: true
        });
        dayOfWeek--;
      }

      // Add days for the current month
      while (date.getMonth() === month) {
        this.weeks.push({
          date: new Date(date),
          today: this.isToday(date)
        });
        date.setDate(date.getDate() + 1);
        dayOfWeek++;

        if (dayOfWeek === this.daysInWeek) {
          // Start a new week
          dayOfWeek = 0;
        }
      }

      // Add days from the next month to fill the last week
      while (dayOfWeek > 0 && dayOfWeek < this.daysInWeek) {
        this.weeks.push({
          date: new Date(year, month + 1, this.daysInWeek - dayOfWeek + 1),
          nextMonth: true
        });
          dayOfWeek++;
        }
        },
          eventsOnDay(date) {
          return this.events.filter(event => {
          return event.date.getDate() === date.getDate() &&
          event.date.getMonth() === date.getMonth() &&
          event.date.getFullYear() === date.getFullYear();
          });
          },
          isToday(date) {
          const today = new Date();
        return (
          date.getDate() === today.getDate() &&
          date.getMonth() === today.getMonth() &&
          date.getFullYear() === today.getFullYear()
      );
    }
  }
};
</script>

<style>
.calendar {
  font-family: sans-serif;
  border-collapse: collapse;
}

.calendar td {
  border: 1px solid #ddd;
  padding: 5px;
  text-align: center;
  height: 80px;
  position: relative;
}

.calendar td.prev-month:before {
  content: attr(data-date);
  display: block;
  color: #bbb;
  font-size: 12px;
  position: absolute;
  top: 5px;
  left: 5px;
}

.calendar td.next-month:before {
  content: attr(data-date);
  display: block;
  color: #bbb;
  font-size: 12px;
  position: absolute;
  top: 5px;
  right: 5px;
}

.calendar td.today {
  background-color: #f2f2f2;
}

.calendar .event {
  background-color: #4CAF50;
  color: white;
  font-size: 12px;
  padding: 2px;
  border-radius: 3px;
  position: absolute;
  bottom: 5px;
  left: 5px;
  right: 5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
