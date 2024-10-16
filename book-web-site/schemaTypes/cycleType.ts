import {defineField, defineType} from 'sanity'

export const cycleType = defineType({
  name: 'cycle',
  title: 'Cycle',
  type: 'document',
  fields: [
    defineField({
      name: 'round',
      type: 'number',
    }),
  ],
})
