<template>
  <div class="bg-light-foreground grid place-items-center gap-y-5 p-5 w-1/2">
    <div class="text-2xl font-semibold">
      {{ formattedTime }}
      {{ isRunning }}
    </div>
    <div class="flex gap-x-3">
      <button
        class="p-1 border hover:bg-light-secondary dark:hover:bg-dark-secondary"
        @click="startTimer"
      >
        Start
      </button>
      <button
        class="p-1 border hover:bg-light-secondary dark:hover:bg-dark-secondary"
        @click="stopTimer"
      >
        Stop
      </button>
      <button
        class="p-1 border hover:bg-light-secondary dark:hover:bg-dark-secondary"
        @click="resetTimer"
      >
        Reset
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      time: 0,
      timer: null,
      isRunning: false,
    };
  },
  computed: {
    formattedTime() {
      let hours = Math.floor(this.time / 3600);
      let minutes = Math.floor((this.time % 3600) / 60);
      let seconds = this.time % 60;

      // Leading zero for values below 10
      hours = hours < 10 ? '0' + hours : hours;
      minutes = minutes < 10 ? '0' + minutes : minutes;
      seconds = seconds < 10 ? '0' + seconds : seconds;

      return `${hours}:${minutes}:${seconds}`;
    },
  },
  methods: {
    startTimer() {
      this.isRunning = true;
      this.timer = setInterval(() => {
        this.time++;
      }, 1000);
    },
    stopTimer() {
      clearInterval(this.timer);
      this.timer = null;
      this.isRunning = false;
    },
    resetTimer() {
      this.stopTimer();
      this.time = 0;
    },
  },
};
</script>
