<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getProfessors, type Professor } from "@/api/professor";
import ProfessorModal from "@/components/modals/ProfessorModal.vue";
import DepartmentSelector from "@/components/DepartmentSelector.vue";

const professors = ref<Professor[]>([]);
const selectedProfessor = ref<Professor | null>(null);
const selectedDepartment = ref<string | null>(null)
const isModalOpen = ref(false);
const searchTerm = ref("");

onMounted(async () => {
  try {
    professors.value = await getProfessors();
    professors.value.sort((a, b) => a.name.localeCompare(b.name));
    console.log(professors);
  } catch (error) {
    console.error("Error fetching professors:", error);
  }
});

const departmentOptions = computed(() => {
  const uniqueDepartments = new Set<string>()
  for (const prof of professors.value) {
    if (prof.department) {
      uniqueDepartments.add(prof.department)
    }
  }
  return Array.from(uniqueDepartments).sort()
})

const filteredProfessors = computed(() => {
  return professors.value.filter((prof) => {
    const checkName = prof.name.toLowerCase().includes(searchTerm.value.toLowerCase());
    const checkDepartment = !selectedDepartment.value || prof.department === selectedDepartment.value;
    return checkName && checkDepartment;
  });
});

function showProfessor(prof: Professor) {
  selectedProfessor.value = prof;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  selectedProfessor.value = null;
}

function updateDepartment(selectedOption: string | null) {
  selectedDepartment.value = selectedOption;
}
</script>

<template>
  <div class="flex flex-col text-primary gap-4 p-4 sm:p-8">
    <div class="flex flex-col items-center gap-2 sm:flex-row sm:justify-center">
      <input
        v-model="searchTerm"
        type="text"
        placeholder="Search by name"
        class="w-64 px-4 py-2 rounded text-black border-2 border-gray-300"
      />
      <DepartmentSelector 
        v-model="selectedDepartment"
        :departments="departmentOptions"
        @update="updateDepartment"
      />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 px-10 pt-1 sm:pt-4">
      <div
        v-for="prof in filteredProfessors"
        :key="prof.email"
      >
        <button
          class="border border-gray-300 rounded hover:bg-green-600 transition-colors duration-200 
            hover:text-white text-500 hover:underline text-center w-full p-4"
          @click="showProfessor(prof)"
          
        >
          {{ prof.name }}
        </button>
      </div>
    </div>

    <ProfessorModal
      v-if="selectedProfessor"
      :prof="selectedProfessor"
      :open="isModalOpen"
      @close="closeModal"
    />
  </div>
</template>