<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div class="centered-boxes">
      <div class="column-section">
        <div class="categoryBox border m-2 mb-4">
          <h3 class="category-title">Can I bring Yacs to my school?</h3>
          <p>Yes! You can view the documentation or contact us to help bring Yacs to your school or University</p>
          <h3 class="category-title">Who can contribute to Yacs?</h3>
          <p>Anyone can contribute to Yacs by creating commits, issues, or pull requests</p>
          <h3 class="category-title">How can I download my course schedule from Yacs?</h3>
          <p>Scroll to the bottom of the schedule page, and select the "Export Data" button next to where your current credit load is displayed</p>
          <h3 class="category-title">Can I see schedules from previous semesters?</h3>
          <p>Yes! You can view, edit, and even create new schedules for prior semesters that have course data uploaded to Yacs</p>
          <h3 class="category-title">Can Yacs tell me if I am ineligble for a course due to my major, minor, or prerequisites?</h3>
          <p>No, at this moment Yacs does not have the capability to tell users this information. If you would like to check this information, we advise looking at SIS or the RPI course website</p>
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
          text: "FAQ",
        },
      ],
    };
  },
};
</script>
  
  <style>
  .gridContainer {
    display: inline-grid;
    grid-template-columns: auto auto;
    justify-content: center;
    align-content: center;
  }
  
  .categoryBox {
    text-align: center;
  }
  
  .category-title {
    color: hsl(211, 100%, 60%);
    background: rgba(108, 90, 90, 0.15);
    border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
  }
  
  .pathway-button {
    display: inline-block;
    background: white;
    border-style: none;
    text-align: justify;
    width: 95%;
  }
  
  .pathway-button:hover {
    background: rgba(108, 90, 90, 0.15) !important;
  }
  
  .courseInPath {
    cursor: pointer;
  }
  
  .courseInPath:hover {
    background-color: rgba(39, 130, 230, 0.5);
  }
  </style>
  