<template>
  <div class="box">
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
</template>

<script>
export default {
  name: 'NoticiaItem',
  props: {
    noticia: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
  },
};
</script>
