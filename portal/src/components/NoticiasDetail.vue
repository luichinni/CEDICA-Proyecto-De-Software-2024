<template>
  <div class="box">
    <article class="media">
      <div class="media-content">
        <div class="content">
          <!-- Mostrar el título de la noticia -->
          <h2 class="title">{{ noticia.titulo }}</h2>

          <!-- Mostrar la fecha y el autor -->
          <p>
            <small>
              Publicado el {{ formatDate(noticia.fecha) }} por {{ noticia.autor }}
            </small>
          </p>

          <!-- Mostrar el resumen (copete) -->
          <p class="has-text-weight-semibold">{{ noticia.copete }}</p>

          <!-- Mostrar el contenido completo de la noticia -->
          <p>{{ noticia.contenido }}</p>
        </div>

        <!-- Botón para volver al listado -->
        <div class="has-text-right">
          <button @click="$emit('volver-al-listado')" class="button is-link">
            Volver al listado
          </button>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
export default {
  name: 'NoticiasDetail',
  props: {
    noticia: {
      type: Object,
      required: true,
    },
  },
  methods: {
    // Formatear la fecha en un formato legible
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
  },
};
</script>
