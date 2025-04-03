<template>
  <v-app>
    <v-main style="margin-top: -4rem; margin-bottom: -3rem">
      <v-container class="aboutContainer my-10">
        <v-card class="pa-6 aboutCard" flat>
          <v-card-title class="subtitle text-center">
            <b>About doccana:</b>
          </v-card-title>
          <v-card-text>
            <p class="text-justify body-text">
              Welcome to <b>doccana</b>, your go-to platform for document annotation and analysis.
              <b>Doccana</b> is a modern, user-friendly platform designed to simplify and streamline
              the annotation process across various use cases: from academic research to real-world
              industry needs.
            </p>
            <h2 class="subtitle">
              <b>Who we are:</b>
            </h2>
            <p class="text-justify body-text">
              We are a team of four ambitious Computer Science students:
              <b>Daniel Palma</b>, <b>Gonçalo Cordeiro</b>, <b>Juary Neto</b>, and
              <b>Steve Rocha</b>, currently pursuing the
              <b>Software Engineering Lab (LES) </b> course unit, at
              <b>University of Algarve (UAlg)</b>. This project is not only part of our academic
              curriculum, but it also reflects our shared passion for
              <b>modern software engineering</b>. We want to show the practical applications of
              <b>doccana</b> and the technologies we have mastered during this and previous units.
            </p>
            <h2 class="subtitle">
              <b>Explaining our project name:</b>
            </h2>
            <p class="text-justify body-text">
              The name <b>doccana</b> is a playful and creative twist on the original open-source
              project <b>doccano</b>, which served as the foundation for our platform. We humorously
              chose the name <b>doccana</b> as a sort of "feminine version" of doccano, a small yet
              meaningful change that reflects our personal touch and spirit of innovation while
              paying homage to the original project that inspired us.
            </p>
            <h2 class="subtitle">
              <b>Why this project?</b>
            </h2>
            <p class="text-justify body-text">
              <b>Doccana</b> was conceived as an
              <b>extension and enhancement of the original open-source project doccano</b>, allowing
              us to build upon a strong foundation while adding our own improvements and custom
              features. It also serves as a <b>showcase of our technical expertise</b>, from
              creating a more intuitive user experience to implementing robust backend
              functionality, and also new possible use cases. This project reflects our ability to
              collaborate, solve complex problems, and deliver a solution tailored to real-world
              needs.
            </p>
            <p class="text-justify body-text">
              This work was proposed by our professors <b>Paula Ventura</b> and
              <b>Néstor Cataño</b>, who taught us the fundamentals of software engineering in lab
              context and provided guidance throughout this journey.
            </p>
            <h2 class="subtitle">
              <b>Our mission:</b>
            </h2>
            <p class="text-justify body-text">
              At <b>doccana</b>, our mission is to
              <b>streamline the document annotation process</b> through a <b>clean, accessible</b>,
              and <b>user-friendly interface</b>. We aim to make annotation easier and more
              efficient for individuals and teams alike, whether for academic, research, or
              industrial purposes. By building upon and extending the functionality of the original
              doccano, we strive to deliver a platform that is not only practical but also enjoyable
              to work with.
            </p>
            <h2 class="subtitle">
              <b>Contact us!</b>
            </h2>
            <p class="text-justify body-text">
              If you have any questions, feedback, or collaboration ideas, feel free to reach out to
              us via email:
            </p>
            <div class="text-center body-text">
              <ul class="contact-list">
                <li><b>Daniel Palma:</b> a71177@ualg.pt</li>
                <li><b>Gonçalo Cordeiro:</b> a76967@ualg.pt</li>
                <li><b>Juary Neto:</b> a76931@ualg.pt</li>
                <li><b>Steve Rocha:</b> a76924@ualg.pt</li>
              </ul>
            </div>
            <p class="text-center final-text mt-6">
              <b>Thank you for visiting doccana.</b> We hope you enjoy your experience on our app
              and find everything you’re looking for. If you have any feedback, please let us know!
              🤗 We’d love to hear from you!
            </p>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.aboutContainer {
  max-width: 840px;
  margin: auto;
}

.aboutCard {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 2rem;
}

.theme--dark .aboutCard {
  background: #1e1e1e;
  color: #f1f1f1;
}

.headline {
  font-family: 'Roboto', sans-serif;
  font-size: 2.8rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 1rem;
}

.subtitle {
  font-family: 'Roboto', sans-serif;
  font-size: 1.8rem;
  font-weight: 320;
  margin-top: 2rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #eeeeee;
  padding-bottom: 0.5rem;
  color: #6376ab;
}

.theme--dark .subtitle {
  border-bottom: 2px solid #333333;
}

.body-text {
  font-family: 'Roboto', sans-serif;
  font-size: 1.05rem;
  line-height: 1.75;
  color: #424242;
  margin-bottom: 4rem;
}

.theme--dark .body-text {
  color: #cccccc;
}

.contact-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.contact-list li {
  margin: 0.5rem 0;
  font-size: 1.05rem;
}

.final-text {
  font-family: 'Roboto', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  margin-top: 2rem;
  color: #616161;
}

.theme--dark .final-text {
  color: #b0b0b0;
}
</style>
