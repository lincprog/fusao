<template>
  <v-snackbar
    :value="hasMessage"
    :color="alert.type"
    @input="clearAlert"
    bottom
  >{{ alert.message }}</v-snackbar>
</template>
<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'SnackBar',
  data () {
    return {
      visible: false
    }
  },
  computed: {
    ...mapState(['alert']),
    hasMessage () {
      return this.alert.message !== ''
    }
  },
  methods: {
    ...mapActions(['clearAlert'])
  }
}
</script>

<style scoped>
</style>
