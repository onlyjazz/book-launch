import {defineField, defineType} from 'sanity'

export const cycleType = defineType({
  name: 'cycle',
  title: 'Cycle',
  type: 'document',
  fields: [
    defineField({
      name: 'key',
      type: 'number',
    }),
    defineField({
      name: 'round',
      type: 'number',
    }),
  ],
})
