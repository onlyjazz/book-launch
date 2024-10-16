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
      name: 'body',
      type: 'array',
      of: [{type: 'block'}],
    }),
    defineField({
      name: 'cycle',
      type: 'number',
    }),
    defineField({
      name: 'cta',
      type: 'url',
    }),
    defineField({
      name: 'date',
      type: 'datetime',
    }),
  ],
})