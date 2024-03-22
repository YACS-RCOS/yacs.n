<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- Your existing content here -->

    <!-- New content with named columns and grey section -->
    <div class="centered-boxes">
      <div class="column-section">
        <!-- Content for the first column -->
        <h3 class="category-title">What is Yacs?</h3>
        <!-- Additional content for column 1 -->
        <p>Yet Another Course Scheduler, or better known as Yacs, is a course scheduler designed to help RPI students plan what courses they will take during each semester.</p>
      </div>
    </div>
    <div class="centered-boxes">
      <div class="column-section">
        <!-- Content for the second column -->
        <h3 class="category-title">What can Yacs do?</h3>
        <!-- Additional content for column 2 -->
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

    <!-- Your existing content here -->

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
  background-color: #f8f9fa; /* Grey background */
  border: 1px solid #ced4da; /* Border color */
  border-radius: 5px; /* Rounded corners */
  padding: 20px; /* Increase padding to add space between border and content */
}

p {
  margin: 10px;
}
</style>
