<template>
    <div class="faq-page">
      <h1>Frequently Asked Questions</h1>
  
      <div v-for="(question, index) in faqData" :key="index" class="faq-item">
        <h3 @click="toggleAnswer(index)">{{ question.title }}</h3>
        <p v-if="question.isOpen">{{ question.answer }}</p>
      </div>
    </div>
</template>
  
<script>
export default {
    name: 'FaqPage',
    data() {
        return {
        faqData: [
            {
                title: 'What is YACS and what is its mission?  1',
                answer: 'A. YACS (Yet Another Course Scheduler) is a web-based application designed to assist students in scheduling and planning their courses at academic institutions. It provides features such as course catalog browsing, schedule building, and course availability information. YACS aims to simplify the course selection process, allowing students to efficiently organize their academic schedules.',
                isOpen: false
            },
            {
                title: 'Q: How can I use the Schedule feature in YACS?',
                answer: 'A: 1.Click the Schedule navbar on the top of the page\n2.Add courses to your schedule by searching for them in the course catalog or using other available options.\n3.Arrange the courses in your preferred time slots or based on your schedule requirements. \n4.YACS will display your scheduled courses, allowing you to visualize your timetable and make adjustments if needed.',
                isOpen: false
            },
            {
                title: 'Q: What is the Explore feature in YACS?',
                answer: 'A:  1.Click the Explore navbar on the top of the page\n2.Choose the major you want to explore from the available options.\n3.YACS will display the courses associated with the selected major for the specified semester.\n4.You can further explore each course for detailed information such as descriptions, prerequisites, and offered sections.',
                isOpen: false
            },
            {
                title: 'Q: How can I use the Pathways Navigation feature in YACS?',
                answer: 'A: 1.Click the Pathways button on the top of the page\n2.Select the pathway you are interested in or that aligns with your academic goals.\n3.YACS will display the pathway requirements and the courses available to fulfill each requirement.\n4.Explore the recommended course options and plan your academic path accordingly.',
                isOpen: false
            },
            {
                title: 'Q: How can I use the Finals feature in YACS?',
                answer: 'A: 1.Click the Finals button on the top of the page\n2.Enter the courses you are enrolled in for the semester. Once you finishing adding your courses, hit Search.\n3.YACS will generate your final exam schedule, displaying the date, time, and location of each exam.',
                isOpen: false
            },
            // Add more FAQ items as needed
        ]
        };
    },
    methods: {
        toggleAnswer(index) {
        this.faqData[index].isOpen = !this.faqData[index].isOpen;
        }
    }
};
</script>

<style>

</style>
