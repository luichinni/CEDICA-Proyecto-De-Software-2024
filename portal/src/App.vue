<template>
  <div class="container mt-5">
    <!-- Sección Home -->
    <section class="hero is-primary is-medium">
      <div class="hero-body">
        <p class="title has-text-centered">CEDICA</p>
        <p class="subtitle has-text-centered">
          Centro de Equitación para Personas con Discapacidad y Carenciadas
        </p>
      </div>
    </section>

    <!-- Enlaces a otras secciones -->
    <section class="section">
      <div class="columns">
        

        <!-- Enlace a Home -->
        <div class="column">
          <div class="card">
            <div class="card-content">
              <h3 class="title is-5">Home</h3>
              <p>Ir a la pagina principal.</p>
              <br>
              <router-link to="/" class="button is-link is-fullwidth mt-3">
                Home
              </router-link>
            </div>
          </div>
        </div>

        <!-- Enlace a Contacto -->
        <div class="column">
          <div class="card">
            <div class="card-content">
              <h3 class="title is-5">Contacto</h3>
              <p>¿Tienes alguna consulta? Ponte en contacto con nosotros.</p>
              <router-link to="/contacto" class="button is-link is-fullwidth mt-3">
                Ir a Contacto
              </router-link>
            </div>
          </div>
        </div>

        <!-- Enlace a Actividades y Noticias -->
        <div class="column">
          <div class="card">
            <div class="card-content">
              <h3 class="title is-5">Actividades y Noticias</h3>
              <p>Mantente informado sobre nuestras actividades y últimas noticias.</p>
              <router-link to="/actividades-noticias" class="button is-link is-fullwidth mt-3">
                Ver Noticias
              </router-link>
            </div>
          </div>
        </div>


      </div>
    </section>
  </div>
  <RouterView />

</template>

<script>
export default {
  name: "App",
};
</script>
