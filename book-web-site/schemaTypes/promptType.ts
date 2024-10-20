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
      name: 'approved',
      type: 'boolean',
    }),
    defineField({
      name: 'cycle',
      type: 'number',
    }),
    defineField({
      name: 'body',
      type: 'array',
      of: [{type: 'block'}],
    }),
    defineField({
      name: 'cta',
      type: 'text',
    }),
    defineField({
      name: 'date',
      type: 'datetime',
    }),
  ],
})