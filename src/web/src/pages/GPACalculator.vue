<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <b-row class="justify-content-md-center">
      <b-col md="5">
        <b-card title="Final Exam Schedule">
          <b-form @submit.prevent="searchExams">
            <div
              v-for="(course, index) in selectedCourses"
              :key="index"
              class="mb-3"
            >
              <b-form-group :label="'Course ' + (index + 1)">
                <b-form-select
                  v-model="selectedCourses[index]"
                  :options="courseOptions"
                ></b-form-select>
              </b-form-group>
            </div>
            <b-button @click="addCourse" variant="primary">Add Course</b-button>
            <b-button type="submit" variant="success" class="ml-3">
              Search
            </b-button>
          </b-form>
          <b-card v-if="examDetails" class="mt-3">
            <h5 class="card-title">Exam Details</h5>
            <div v-for="exam in examDetails" :key="exam.id">
              <div>
                <strong>Course:</strong>
                {{ exam.course }}
              </div>
              <div>
                <strong>Section:</strong>
                {{ exam.section }}
              </div>
              <div>
                <strong>Room:</strong>
                {{ exam.room }}
              </div>
              <div>
                <strong>Time:</strong>
                {{ exam.time }}
              </div>
              <div>
                <strong>Date:</strong>
                {{ exam.day }}, {{ exam.dayOfWeek }}
              </div>
              <hr v-if="exam !== examDetails[examDetails.length - 1]" />
            </div>
          </b-card>
        </b-card>
      </b-col>
      <b-col md="7">
        <calendar :exam-details="examDetails"></calendar>
      </b-col>
    </b-row>
  </b-container>
</template>