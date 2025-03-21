<script setup lang="ts">
import GenericModal from "@/components/modals/GenericModal.vue";
import { useAsyncState, useFileDialog } from "@vueuse/core";
import type { AxiosError } from "axios";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router/auto";

const props = defineProps<{
  acceptFileTypes: string;
  action: (v: File) => Promise<unknown>;
  disallowMultipleFiles?: boolean;
  title: string;
}>();

const emit = defineEmits<{
  uploadSuccess: [file: string];
  uploadError: [error: [string, AxiosError]];
}>();

const router = useRouter();

const filedialog = useFileDialog({
  accept: props.acceptFileTypes,
  multiple: !props.disallowMultipleFiles
});

const filebutton = ref<HTMLInputElement | null>(null);

const uploadstatus = useAsyncState(
  async (filelist: FileList) => {
    const result = await Promise.allSettled(
      Array.from(filelist).map((v) =>
        props
          .action(v)
          .then(() => {
            emit("uploadSuccess", v.name);
          })
          .catch((e) => {
            emit("uploadError", e as [string, AxiosError]);
            // eslint-disable-next-line @typescript-eslint/only-throw-error
            throw [v.name, e];
          })
      )
    );

    const errors = result.filter((v) => v.status == "rejected");
    if (errors.length > 0) {
      // eslint-disable-next-line @typescript-eslint/only-throw-error
      throw errors;
    } else {
      return result;
    }
  },
  [],
  {
    immediate: false,
    resetOnExecute: true
  }
);

filedialog.onChange((files) => {
  if (files && files.length > 0) {
    filebutton.value?.setCustomValidity("");
  } else {
    filebutton.value?.setCustomValidity("Please add a file");
  }
});

onMounted(() => {
  filebutton.value?.setCustomValidity("Please add a file");
});

function onSubmit(ev: Event) {
  if (ev.target) {
    const filelist = filedialog.files.value;
    if ((ev.target as HTMLFormElement).checkValidity() && filelist) {
      void uploadstatus.execute(0, filelist);
    }
    return true;
  }
  return false;
}
</script>

<template>
  <GenericModal
    v-slot="{
      //close
    }"
    :open="true"
    @close="
      () => {
        if (!uploadstatus.isLoading.value) {
          router.back();
        }
      }
    "
  >
    <form
      class="flex flex-col items-center justify-between gap-4 p-5"
      @submit.prevent="onSubmit($event)"
    >
      <h2 class="text-4xl font-bold">{{ props.title }}</h2>
      <button
        ref="filebutton"
        type="submit"
        class="bg-secondary rounded-sm p-2 disabled:brightness-75"
        :disabled="uploadstatus.isLoading.value"
        @click.prevent="
          () => {
            filedialog.open();
          }
        "
      >
        Choose file
        <p v-if="filedialog.files.value">
          (selected file{{ filedialog.files.value.length > 1 ? "s" : "" }}:

          <template
            v-for="(file, i) in filedialog.files.value"
            :key="file.name"
          >
            {{ file.name + (i + 1 < filedialog.files.value.length ? ", " : "") }} </template
          >)
        </p>
      </button>
      <button
        type="submit"
        class="rounded-sm bg-green-500 p-2 disabled:brightness-75"
        :disabled="uploadstatus.isLoading.value"
      >
        <template v-if="uploadstatus.isLoading.value">
          <div class="bg-primary mask-image-multiselect-spinner aspect-square h-4 animate-spin" />
        </template>
        <template v-else> Submit </template>
      </button>
    </form>
  </GenericModal>
</template>
