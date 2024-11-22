<template>
  <section class="section">
    <div class="container">
      <h2 class="title is-3 has-text-centered">Actividades y Noticias</h2>
      <p class="subtitle has-text-centered">
        Descubre nuestras últimas actividades y noticias.
      </p>

      <Search 
        v-if="!noticiaSeleccionada" 
        :total="total"
        :pages="pages"
        :current_page="current_page"
        :per_page="per_page"
        :items="noticias" 
        :loading="loading" 
        :error="error" 
        :nombre_elementos="'noticias'"
        @search="handleSearch" 
        @ver-detalle="verDetalle" 
        @change-page="changePage" 
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
import Search from '../components/search/Search.vue';
import NoticiasDetail from '../components/NoticiasDetail.vue';
import axios from 'axios';
import { noticias_route } from '../router/api_routes';

export default {
  name: 'ActividadesNoticiasView',
  components: {
    Search,
    NoticiasDetail,
  },
  data() {
    return {
      //Datos
      noticias: [],

      //Datos de filtrado
      current_search_data : {
        author : "", 
        published_from : "", 
        published_to : "", 
      },

      //Informacion sobre la paginacion
      total : 0,
      pages : 2,
      current_page : 1,
      per_page : 5,

      //Informacion sobre la carga de datos
      loading: false,
      error: null,
      noticiaSeleccionada: null,
    };
  },
  methods: {
    // Cargar noticias desde la API
    async fetchNoticias(search_data = this.current_search_data, page = this.current_page, per_page = this.per_page) {
      try {
        this.loading = true; 
        this.error = null; 

        const response = await axios.get(noticias_route, {
          params: {
            ...search_data, 
            page,           
            per_page,       
          }
        });  
        this.total = response.data.total;
        this.pages = response.data.pages;
        this.current_page = response.data.current_page;
        this.per_page = response.data.per_page;
        this.noticias = response.data.publications.sort((a, b) => new Date(b.fecha_publicacion) - new Date(a.fecha_publicacion));
        
        //this.noticias = response.data.sort((a, b) => new Date(b.fecha_publicacion) - new Date(a.fecha_publicacion));
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
    handleSearch(search_data) {
      this.current_search_data = search_data; 
    },
    changePage(page) {
      this.current_page = page; 
    },
  },
  watch: {
    current_search_data(newSeachData) {
      this.fetchNoticias(newSeachData, this.current_page, this.per_page);
    },
    current_page(newPage) {
      this.fetchNoticias(this.current_search_data, newPage, this.per_page);
    },
    per_page(newPerPage) {
      this.fetchNoticias(this.current_search_data, this.current_page, newPerPage);
    },
  },
  created() {
    this.fetchNoticias();
  },
};
</script>
