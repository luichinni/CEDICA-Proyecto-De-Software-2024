<template>
  <div v-if="loading" class="has-text-centered">
    <button class="button is-loading is-primary is-large">Cargando...</button>
  </div>

  <div v-else-if="error" class="notification is-danger has-text-centered">
    <p>⚠️ Error al cargar las noticias: {{ error }}</p>
  </div>


  <div v-if="!loading && noticias.length" class="mt-5">
    <NoticiaItem 
      v-for="(noticia, index) in noticias" 
      :key="index" 
      :noticia="noticia" 
      @ver-detalle="$emit('ver-detalle', noticia)"
    />
  </div>
  <p v-if="!loading && !noticias.length"> No hay noticias disponibles. </p>
</template>

<script>
import NoticiaItem from './NoticiaItem.vue';

export default {
  name: 'NoticiasList',
  components: {
    NoticiaItem,
  },
  props: {
    noticias: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      required: true,
    },
    error: {
      type: String,
      required: false,
      default: null,
    },
  },
};
</script>
