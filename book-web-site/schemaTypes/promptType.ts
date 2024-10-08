import {defineField, defineType} from 'sanity'

export const promptType = defineType({
  name: 'prompt',
  title: 'Prompt',
  type: 'document',
  fields: [
    defineField({
      name: 'header',
      type: 'string',
    }),
    defineField({
      name: 'body',
      type: 'array',
      of: [{type: 'block'}],
    }),
    defineField({
      name: 'dow',
      type: 'number',
    }),
    defineField({
      name: 'date',
      type: 'datetime',
    }),
  ],
})