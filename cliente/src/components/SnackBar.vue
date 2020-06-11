<template>
  <div>
    <v-snackbar
      :value="hasSuccessMessage"
      color="success"
      @close="dismiss('success')"
      multi-line
      bottom>{{ messages.success }}</v-snackbar>

    <v-snackbar
      :value="hasErrorMessages"
      color="error"
      @close="dismiss('error')"
      multi-line
      bottom>{{ formatedErrorMessage }}</v-snackbar>

    <v-snackbar
      :value="hasValidationMessages"
      color="warning"
      @close="dismiss('validation')"
      multi-line
      bottom>{{ formatedValidationMessage }}</v-snackbar>

  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'SnackBar',
  computed: {
    ...mapState(['messages']),
    hasSuccessMessage () {
      return this.messages.success !== ''
    },
    hasErrorMessages () {
      return this.messages.error.length > 0
    },
    hasValidationMessages () {
      return this.messages.validation.length > 0
    },
    formatedErrorMessage () {
      return this.messages.error.join(',')
    },
    formatedValidationMessage () {
      return this.messages.validation.join(',')
    }
  },
  methods: {
    ...mapActions(['setMessage']),
    dismiss (type) {
      let obj
      if (type === 'error') {
        obj = { type, message: [] }
      } else if (type === 'validation') {
        obj = { type, message: {} }
      } else {
        obj = { type, message: '' }
      }
      this.setMessage(obj)
    }
  }
}
</script>

<style scoped>
</style>
