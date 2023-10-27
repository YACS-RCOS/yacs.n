<template>
    <div class="faq-page">
      <h1>Frequently Asked Questions</h1>
  
      <div v-for="(question, index) in faqData" :key="index" class="faq-item">
        <div class="question-wrapper" @click="toggleAnswer(index)">
          <h3 :class="{ 'active': question.isOpen }">{{ question.title }}</h3>
          <div class="dropdown-indicator">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-chevron-down">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
        </div>
        <div class="divider"></div>
        <div class="answer-wrapper" :class="{ 'open': question.isOpen }" :style="{'max-height': question.maxheight }">
          <p v-if="question.isOpen">{{ question.answer}}</p>
          <p v-if="question.isOpen">{{ question.answer1}}</p>
          <p v-if="question.isOpen">{{ question.answer2,}}</p>
          <p v-if="question.isOpen">{{ question.answer3}}</p>
        </div>
      </div>
    </div>
  </template>
  
<script>
export default {
    name: 'FAQs',
    data() {
        return {
        faqData: [
            {
                title: 'What is YACS and what is its mission?',
                answer_symbol: 'A:',
                answer:' YACS (Yet Another Course Scheduler) is a web-based application designed to assist students in scheduling and planning their courses at academic institutions. It provides features such as course catalog browsing, schedule building, and course availability information. YACS aims to simplify the course selection process, allowing students to efficiently organize their academic schedules.',
                isOpen: false
            },
            {
                title: 'How can I use the Schedule feature?',
                answer_symbol: 'A:',
                answer:'1. Click the Schedule navbar on the top of the page.',
                answer1:'2. Add courses to your schedule by searching for them in the course catalog or using other available options.',
                answer2:'3. Arrange the courses in your preferred time slots or based on your schedule requirements.',
                answer3:'4. YACS will display your scheduled courses, allowing you to visualize your timetable and make adjustments if needed.',
                isOpen: false
            },
            {
                title: 'What is the Explore feature?',
                answer_symbol: 'A:',
                answer:'1. Click the Explore navbar at the top of the page.' ,
                answer1:'2. Choose the major you want to explore from the available options. ',
                answer2:'3. YACS will display the courses associated with the selected major for the specified semester.',
                answer3:'4. You can further explore each course for detailed information such as descriptions, prerequisites, and offered sections.',
                isOpen: false
            },
            {
                title: 'How can I use the Pathways Navigation feature?',
                answer_symbol: 'A:',
                answer:'1. Click the Pathways button at the top of the page.',
                answer1:'2. Select the pathway you are interested in or that aligns with your academic goals.',
                answer2:'3. YACS will display the pathway requirements and the courses available to fulfill each requirement.',
                answer3:'4. Explore the recommended course options and plan your academic path accordingly.',
                isOpen: false
            },
            {
                title: 'How can I use the Finals feature?',
                answer_symbol: 'A:',
                answer:'1. Click the Finals button on the top of the page.',
                answer1:'2. Enter the courses you are enrolled in for the semester. Once you finish adding your courses, hit Search.',
                answer2:'3. YACS will generate your final exam schedule, displaying the date, time, and location of each exam.',
                isOpen: false
            },
            // Add more FAQ items as needed
        ]
        };
  },
  methods: {
    toggleAnswer(index) {
      this.faqData[index].isOpen = !this.faqData[index].isOpen;
    },
  },
};
</script>

<style scoped>
.faq-page {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.faq-item {
  margin-bottom: 20px;
  border: 3px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  cursor: pointer;
}

.faq-item:hover {
  border-color: hsl(211, 100%, 60%);
}

.question-wrapper {
  margin-bottom: 10px;
}

.faq-item h3 {
  font-size: 18px;
  margin: 0;
  color: #333;
  font-weight: bold;
  cursor: pointer;
}

.faq-item h3.active {
  text-decoration: underline;
}

.divider {
  height: 1px;
  background-color: #ccc;
}

.answer-wrapper {
  margin-top: 10px;
  max-height:0;
  overflow: hidden;
  transition: max-height 0.3s ease-in-out;
}

.answer-wrapper.open {
  max-height: 1000px; /*Adjust the value to a sufficiently large value to ensure full visibility*/
}

.faq-item p {
  font-size: 14px;
  color: #555;
  opacity: 0.3s;
  transition: opacity 0.3s ease-in-out;
}

.faq-item.open p {
  opacity: 1;
}

.dropdown-indicator {
  width: 20px;
  height: 20px;
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  transition: transform 0.3s ease;
}
.open .dropdown-indicator {
  transform: rotate(180deg);
  width: 20px;
  height: 20px;
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  transition: transform 0.3s ease;
}
</style>