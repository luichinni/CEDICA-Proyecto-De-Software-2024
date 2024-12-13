<template>
  <section class="section">
    <div class="container">
      <!-- Caja con sombra y borde redondeado -->
      <div class="box">
        <h2 class="title is-3 has-text-centered">Ponte en contacto con nosotros</h2>
        <p class="subtitle has-text-centered">¡Nos encantaría saber de ti!</p>

        <div id="success-msg">
          <div v-if="success" class="notification is-info">
            Tu mensaje nos ha llegado con éxito, te responderemos en cuanto podamos! 💙
          </div>
        </div>
        <div id="error-msg">
          <div v-if="notsuccess" class="notification is-danger">
            Ups, parece que no pudimos enviar tu mensaje, intenta nuevamente!😔
          </div>
        </div>

        <!-- Formulario de contacto -->
        <form @submit="enviar_form">
          <div class="field">
            <label class="label">Asunto 🤔 *</label>
            <div class="control">
              <input required class="input" type="text" placeholder="¿Por que motivo quieres contactarnos?" v-model="title" />
            </div>
          </div>

          <div class="field">
            <label class="label">Email de contacto 📧 *</label>
            <div class="control">
              <input required class="input" type="email" placeholder="Dejanos tu email para poder responderte" v-model="email" />
            </div>
          </div>

          <div class="field">
            <label class="label">Mensaje 💬 *</label>
            <div class="control">
              <textarea required class="textarea" placeholder="Escribe tu mensaje aquí" v-model="description"></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">Captcha *</label>

            <figure class="image is-9by3" style="max-width: 50%; border-radius:1%;">
              <img :src="captcha64" alt="Cargando captcha...">
            </figure>
            <br/>
            <div class="control">
              <input required class="input" placeholder="Ingresa el texto de la imagen" v-model="captcha_rta" />
            </div>
          </div>

          <div v-if="captcha_error" class="notification is-warning">
            {{ flash }}
          </div>

          <div class="field is-grouped is-justify-content-center">
            <div class="control">
              <button class="button is-link">Enviar</button>
            </div>
            <div class="control">
              <router-link to="/" class="button is-light">
                Cancelar
              </router-link>
            </div>
          </div>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import { captcha_route, contacto_route } from "@/router/api_routes";

const captcha64 = ref("")

const title = ref("")
const email = ref("")
const description = ref("")
const captcha_rta = ref("")

const captcha_error = ref(false)
const flash = ref("")

const success = ref(false)
const notsuccess = ref(false)

let token = null

function show_success(){
  success.value = !success.value;
  if (success.value){
    setTimeout(show_success, 10000); // para poner en false el mensaje despues de 10 segundos

    let msgElem = document.getElementById("success-msg");
    msgElem.scrollIntoView({behavior: "smooth", block: "center"});

    // Reset
    title.value = ""
    email.value = ""
    description.value = ""
    load_captcha()
  }
}

function show_error(){
  notsuccess.value = !notsuccess.value;
  if (notsuccess.value){
    setTimeout(show_error, 10000); // para poner en false el mensaje despues de 10 segundos

    let msgElem = document.getElementById("error-msg");
    msgElem.scrollIntoView({behavior: "smooth", block: "center"});

    // Reset
    load_captcha()
  }
}

async function load_captcha(){
  captcha_rta.value = ""
  let res = await axios.get(captcha_route);

  captcha64.value = res.data.captcha;
  token = res.data.token;
}

onMounted(async () => {
  load_captcha()
});

async function enviar_form(e){
  e.preventDefault();

  /////////////////////////////////////////
  // Validación del captcha
  /////////////////////////////////////////

  let rta = {
    "token": token,
    "word": captcha_rta.value
  }

  let captcha_res = (await axios.post(
    captcha_route,
    rta
  )).data['result'];

  /////////////////////////////////////////
  // Envio del formulario
  /////////////////////////////////////////
  if (captcha_res){
    const ISO_date = (new Date()).toISOString();

    let info_contacto = {
      "title": title.value,
      "email": email.value,
      "description": description.value
    }

    axios.post(
      contacto_route,
      info_contacto
    ).then(()=>{
      show_success()
    }).catch(()=>{
      show_error()
    })
    
  }else{
    captcha_error.value = true;
    flash.value = "Captcha incorrecto, intenta nuevamente!!";
    load_captcha();
    setTimeout(remove_error, 5000);
  }
}

function remove_error(){
  captcha_error.value = false;
}

</script>
