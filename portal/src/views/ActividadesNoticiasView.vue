<template>
  <section class="section">
    <div class="container">
      <h2 class="title is-3 has-text-centered">Actividades y Noticias</h2>
      <p class="subtitle has-text-centered">
        Descubre nuestras últimas actividades y noticias.
      </p>

      <NoticiasList 
        v-if="!noticiaSeleccionada" 
        :noticias="noticias" 
        :loading="loading" 
        :error="error" 
        @ver-detalle="verDetalle" 
      />
      
      <NoticiasDetail 
        v-else 
        :noticia="noticiaSeleccionada" 
        @volver-al-listado="volverAlListado" 
      />
    </div>
  </section>
</template>

<script>
import NoticiasList from '../components/NoticiasList.vue';
import NoticiasDetail from '../components/NoticiasDetail.vue';
import axios from 'axios';
import { noticias_route } from '../router/api_routes';

export default {
  name: 'ActividadesNoticiasView',
  components: {
    NoticiasList,
    NoticiasDetail,
  },
  data() {
    return {
      noticias: [],
      loading: false,
      error: null,
      noticiaSeleccionada: null,
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
    verDetalle(noticia) {
      this.noticiaSeleccionada = noticia;
    },
    volverAlListado() {
      this.noticiaSeleccionada = null;
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
