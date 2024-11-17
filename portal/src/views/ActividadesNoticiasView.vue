<script setup>
  import NoticiasList from '../components/NoticiasList.vue';
</script>

<template>
  <section class="section">
    <div class="container">

      <h2 class="title is-3 has-text-centered">Actividades y Noticias</h2>
      <p class="subtitle has-text-centered">
        Descubre nuestras últimas actividades y noticias.
      </p>

      <!-- Listado de Noticias -->
      <NoticiasList :noticias="noticias" :loading="loading" :error="error" />

    </div>
  </section>
</template>

<script>

import axios from 'axios';
import { noticias_route } from '../router/api_routes';
export default {
  name: 'ActividadesYNoticias',
  data() {
    return {
      noticias: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    // Cargar noticias desde la API
    async fetchNoticias() {
      try {
        this.loading = true; 
        this.error = null; 
        const response = await axios.get(noticias_route); 
        this.noticias = response.data.sort((a, b) => new Date(b.fecha_publicacion) - new Date(a.fecha_publicacion));
      } catch (error) {
        this.error = 'Error al cargar las noticias'
        console.error('Error al cargar las noticias:', error);
      } finally {
        this.loading = false
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
