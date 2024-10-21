import {defineField, defineType} from 'sanity'

export const promptType = defineType({
  name: 'prompt',
  title: 'Prompt',
  type: 'document',
  fields: [
    defineField({
      name: 'identifier',
      type: 'string',
    }),
    defineField({
      name: 'approved',
      type: 'boolean',
    }),
    defineField({
      name: 'impression_count',
      type: 'number',
    }),
    defineField({
      name: 'engagement_rate',
      type: 'number',
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