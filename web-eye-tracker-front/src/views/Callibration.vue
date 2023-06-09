<template>
  <div id="box">
    <Toolbar />
    <v-container class="mt-12">
      <v-row justify="center" align="start">
        <v-col cols="12" lg="5" md="5">
          <v-card outlined>
            <v-card-title>
              <v-icon left>mdi-information</v-icon>
              Calibration System
            </v-card-title>
            <p class="mx-4">
              The calibration works by associating the position of your eyes' iris with the coordinates
              of the circle on the screen.
              <br><br>
              Before starting the process, turn on the camera and make sure your face and eyes
              are being captured by the model. After clicking start please don't leave the current position.
              <br><br>
              Your task during the calibration is to follow the circles with your eyes. Try your best to not look away and to keep following. Blinking is fine.
            </p>
            <v-card-actions class="px-4 mt-12 mb-4">
              <v-btn block outlined color="green" :disabled="!isCameraOn" @click="goToCallibRecord()"
                >Start Callibration</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" lg="7" md="7">
          <v-row justify="center" class="ma-0">
            <v-btn
              @click="setupCamera()"
              v-if="!isCameraOn"
              outlined
              color="blue"
            >
              Turn camera on
              <v-icon right size="20">mdi-camera-outline</v-icon>
            </v-btn>
          </v-row>
          <div v-if="!isModelLoaded && isCameraOn">
            <v-row justify="center" class="mt-8" align="center">
              <v-progress-circular
                :size="50"
                :width="7"
                color="black"
                indeterminate
              ></v-progress-circular>
              <h2 class="ml-4">Loading model...</h2>
            </v-row>
          </div>
          <video autoplay id="video-tag" style="display: none"></video>
          <canvas id="canvas" width="600px" height="500px" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Toolbar from "@/components/Toolbar.vue";
const tf = require("@tensorflow/tfjs");
const faceLandmarksDetection = require("@tensorflow-models/face-landmarks-detection")

export default {
  components: {
    Toolbar,
  },
  data() {
    return {
      isCameraOn: false,
      model: null,
      predictions: [],
      isModelLoaded: false,
      webcamStream: null
    };
  },
  watch: {
    predictions: {
      handler() {
        this.detectFace();
      },
      deep: true,
    },
  },
  methods: {
    goToCallibRecord() {
        this.webcamStream.getTracks().forEach((track) => {
          track.stop()
        })
        this.$router.push('/callibration/record')
    },
    setupCamera() {
      let video = document.getElementById("video-tag");
      navigator.mediaDevices
        .getUserMedia({
          audio: false,
          video: { width: 600, height: 500 },
        })
        .then(async (stream) => {
          // stream is a MediaStream object
          video.srcObject = stream;
          this.isCameraOn = true;

          this.webcamStream = stream

          await tf.getBackend();
          // Load the faceLandmarksDetection model assets.
          this.model = await faceLandmarksDetection.load(faceLandmarksDetection.SupportedPackages.mediapipeFacemesh);

          this.isModelLoaded = true;
          this.detectFace();
        });
    },
    async detectFace() {
      let video = document.getElementById("video-tag");
      let canvas = document.getElementById("canvas");
      let ctx = canvas.getContext("2d");
      
      this.predictions = await this.model.estimateFaces({
        input: document.getElementById("video-tag")
      });

      // draw the video first
      ctx.drawImage(video, 0, 0, 600, 500);
      this.predictions.forEach((pred) => {
        // draw the rectangle enclosing the face
        ctx.fillStyle = "red";

        // left iris
        ctx.fillRect(
          pred.scaledMesh[468]['0'],
          pred.scaledMesh[468]['1'],
          5,5
        );

        // right iris
        ctx.fillRect(
          pred.scaledMesh[473]['0'],
          pred.scaledMesh[473]['1'],
          5,5
        );
        
        // face contour
        ctx.beginPath();
        ctx.lineWidth = "4";
        ctx.strokeStyle = "blue";
        ctx.rect(
          pred.boundingBox.topLeft[0],
          pred.boundingBox.topLeft[1],
          pred.boundingBox.bottomRight[0] - pred.boundingBox.topLeft[0],
          pred.boundingBox.bottomRight[1] - pred.boundingBox.topLeft[1]
        );
        ctx.stroke();

      });
    },
  },
};
</script>
