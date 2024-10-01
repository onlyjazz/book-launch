import {defineField, defineType} from 'sanity'

export const postType = defineType({
  name: 'post',
  title: 'Post',
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
      name: 'response',
      type: 'markdown'
    }),
    defineField({
      name: 'date',
      type: 'datetime',
    }),
    defineField({
      name: 'cta',
      type: 'url',
    }),
    defineField({
      name: 'image',
      type: 'image',
    })
  ],
})