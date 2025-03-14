<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { getProfessors, type Professor } from "@/api/professor";
import ProfessorModal from "@/components/modals/ProfessorModal.vue";

const professors = ref<Professor[]>([]);
const selectedProfessor = ref<Professor | null>(null);
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

const filteredProfessors = computed(() => {
  if (!searchTerm.value) return professors.value;
  return professors.value.filter((prof) =>
    prof.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

function showProfessor(prof: Professor) {
  selectedProfessor.value = prof;
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
  selectedProfessor.value = null;
}
</script>

<template>
  <div class="flex flex-col text-primary gap-4 p-4">

    <div class="mb-3 flex justify-center">
      <input
        v-model="searchTerm"
        type="text"
        placeholder="Search by name"
        class="w-64 px-4 py-2 text-lg border border-gray-400 rounded text-black"
      />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 px-10">
      <div
        v-for="prof in filteredProfessors"
        :key="prof.email"
        class="border border-gray-300 rounded p-4"
      >
        <button
          class="text-500 hover:underline text-center w-full"
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
