<template>
  <v-dialog v-model="dialog" width="50%" :fullscreen="$vuetify.breakpoint.xsOnly">
    <v-card>
      <v-card-title>Analyze this sample?</v-card-title>
      <v-card-text>We've recorded both your screen and your webcam during the recording time. We need your consent to analyze the videos to create the reports. Do you consent?</v-card-text>
      <v-card-actions>
        <v-spacer/>
        <v-btn outlined color="red" @click="no">No</v-btn>
        <v-btn dark color="success" @click="yes">Yes</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
  export default {
    props:['dialog','consent'],
    methods: {
      yes() {
        this.$emit('consent', true)
        this.$emit('dialog', false)
      },
      no() {
        this.$emit('consent', false)
        this.$emit('dialog', false)
      }
    }
  }
</script>
