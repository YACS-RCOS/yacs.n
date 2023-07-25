<template>
    <div class="faq-page">
      <h1>Frequently Asked Questions</h1>
  
      <div v-for="(question, index) in faqData" :key="index" class="faq-item" :class="{ 'active-item': question.isOpen }">
        <div class="question-wrapper">
          <h3 @click="toggleAnswer(index)">{{ question.title }}</h3>
        </div>
        <div class="divider"></div>
        <div class="answer-wrapper">
          <p v-if="question.isOpen">{{ question.answer_symbol}}</p>
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
                title: 'Q: What is YACS and what is its mission?',
                answer_symbol: 'A:',
                answer:' YACS (Yet Another Course Scheduler) is a web-based application designed to assist students in scheduling and planning their courses at academic institutions. It provides features such as course catalog browsing, schedule building, and course availability information. YACS aims to simplify the course selection process, allowing students to efficiently organize their academic schedules.',
                isOpen: false
            },
            {
                title: 'Q: How can I use the Schedule feature?',
                answer_symbol: 'A:',
                answer:'1.Click the Schedule navbar on the top of the page.',
                answer1:'2.Add courses to your schedule by searching for them in the course catalog or using other available options.',
                answer2:'3.Arrange the courses in your preferred time slots or based on your schedule requirements.',
                answer3:'4.YACS will display your scheduled courses, allowing you to visualize your timetable and make adjustments if needed.',
                isOpen: false
            },
            {
                title: 'Q: What is the Explore feature?',
                answer_symbol: 'A:',
                answer:'1.Click the Explore navbar at the top of the page.' ,
                answer1:'2.Choose the major you want to explore from the available options. ',
                answer2:'3.YACS will display the courses associated with the selected major for the specified semester.',
                answer3:'4.You can further explore each course for detailed information such as descriptions, prerequisites, and offered sections.',
                isOpen: false
            },
            {
                title: 'Q: How can I use the Pathways Navigation feature?',
                answer_symbol: 'A:',
                answer:'1.Click the Pathways button at the top of the page.',
                answer1:'2.Select the pathway you are interested in or that aligns with your academic goals.',
                answer2:'3.YACS will display the pathway requirements and the courses available to fulfill each requirement.',
                answer3:'4.Explore the recommended course options and plan your academic path accordingly.',
                isOpen: false
            },
            {
                title: 'Q: How can I use the Finals feature?',
                answer_symbol: 'A:',
                answer:'1.Click the Finals button on the top of the page.',
                answer1:'2.Enter the courses you are enrolled in for the semester. Once you finish adding your courses, hit Search.',
                answer2:'3.YACS will generate your final exam schedule, displaying the date, time, and location of each exam.',
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
    }
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
  font-size: 24px;
  margin-bottom: 20px;
}

.faq-item {
  margin-bottom: 20px;
  border: 3px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
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
}

.divider {
  height: 1px;
  background-color: #ccc;
  transition: opacity 0.3s ease;
}

.answer-wrapper {
  margin-top: 10px;
}

.faq-item p {
  display: none;
  font-size: 14px;
  color: #555;
}

.faq-item.active-item p {
  display: block;
}
</style>