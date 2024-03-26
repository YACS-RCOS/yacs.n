<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div class="centered-boxes">
      <div class="column-section">
        <div class="categoryBox border m-2 mb-4">
          <h3 class="category-title">What is Yacs?</h3>
          <p>Yet Another Course Scheduler, or better known as Yacs, was created with the goal of making students' lives a little easier. It allows users to avoid the clunky UIs of proprietary Catalog Management and Student Information Systems, replacing these unpleasant experiences with easy browsing and searching of courses, and adds the additional functionality of easy schedule generation, and much more.</p>
          <p>But Yacs has grown to be much more than a simple schedule generator. Our mission at Yacs is the following:</p>
          <ol>
            <li class = li-inner-element>To alleviate the stress around academic and extracurricular planning for Students, Faculty and Staff by offering a free, easy-to-use interface to supplement or replace traditional academic information and management systems.</li>
            <li class = li-inner-element>To enable innovative, disruptive applications in the academic space by breaking down proprietary information silos and providing consistent, digestible, Open Data.</li>
            <li>To empower students to take control of their academic experience and excel their careers through learning about and contributing to Open Source.</li>
          </ol>
          <p>Further, Yacs aims to provide the best experience possible to as many people as possible by serving as many universities as we can. Yacs is built from the ground up to be modular and flexible, and as such can use data from any source, and even combine data from many sources in an intelligent way.</p>
          <p>We have made it as easy as possible to connect Yacs to your university, and have designed this process to be accessible to developers of nearly any skill level. Please read through this documentation or contact us if you'd like to bring Yacs to your school, and help us make Yacs as great as it can be.</p>
          <p>Yacs owes its creation and continued maintenance to <a href="https://new.rcos.io/">RCOS</a>, the Rensselaer Center for Open Source, and is developed in collaboration with <a href="https://bugsnyu.com/">BUGS</a>, NYU&apos;s Open Source Club.</p>
        </div>
      </div>
    </div>
    <div class="centered-boxes">
      <div class="column-section">
        <div class="categoryBox border m-2 mb-4">
          <h3 class="category-title">What can Yacs do?</h3>
          <p>Yacs has a variety of features that include but are not limited to:</p>
          <ul>
            <li>Allow students to view courses from the current and previous semesters</li>
            <li>Allow students to create a mock schedule using their desired courses</li>
            <li>Allow students to view information and requirements of current HASS pathways</li>
            <li>Allow students to view information on RPI professors</li>
            <li>Allow students to make a mock schedule for their final exams</li>
          </ul>
        </div>
      </div>
    </div>
  </b-container>
</template>



<script>
export default {
data() {
  return {
    breadcrumbNav: [
      {
        text: "YACS",
        to: "/",
      },
      {
        text: "About",
      },
    ],
  };
},
};
</script>

<style>
.category-title {
  color: hsl(211, 100%, 60%);
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1) solid 1px;
  padding: 10px; /* Add padding to match the background */
  margin-top: 0; /* Remove default margin */
}

.centered-boxes {
  display: flex;
  justify-content: center;
  margin-bottom: 20px; /* Adjust spacing between boxes */
}

.column-section {
  width: 70%;
}

p {
  margin: 10px;
}

.li-inner-element {
  padding-bottom: 10px;
}
</style>
