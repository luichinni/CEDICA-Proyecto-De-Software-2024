<template>
  <section class="section">
    <div class="container">
      <!-- Título Principal -->
      <h2 class="title is-3 has-text-centered">Actividades y Noticias</h2>
      <p class="subtitle has-text-centered">
        Descubre nuestras últimas actividades y noticias.
      </p>

      <!-- Listado de Noticias -->
      <div v-if="noticias.length" class="mt-5">
        <div v-for="(noticia, index) in noticias" :key="index" class="box">
          <article class="media">
            <div class="media-content">
              <div class="content">
                <p>
                  <strong>{{ noticia.titulo }}</strong>
                  <br />
                  <small>{{ formatDate(noticia.fecha_publicacion) }}</small>
                  <br />
                  <em>{{ noticia.copete }}</em>
                </p>
              </div>
              <!-- Enlace para ver la nota completa -->
              <div class="has-text-right">
                <router-link :to="`/noticia/${noticia.id}`" class="button is-link is-small">
                  Leer más
                </router-link>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- Mensaje cuando no hay noticias -->
      <div v-else class="notification is-warning has-text-centered">
        No hay noticias disponibles en este momento.
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ActividadesYNoticias',
  data() {
    return {
      noticias: [],
    };
  },
  methods: {
    // Cargar noticias desde la API
    async fetchNoticias() {
      try {
        const response = await axios.get('/api/noticias'); // Ajusta la URL según tu backend
        this.noticias = response.data.sort((a, b) => new Date(b.fecha_publicacion) - new Date(a.fecha_publicacion));
      } catch (error) {
        console.error('Error al cargar las noticias:', error);
      }
    },
    // Formatear fecha a un formato legible
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
  },
  created() {
    this.fetchNoticias();
  },
};
</script>

<style>
.section {
  padding-top: 3rem;
  padding-bottom: 3rem;
}
</style>
