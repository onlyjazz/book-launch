import {defineField, defineType} from 'sanity'

export const postType = defineType({
  name: 'post',
  title: 'Post',
  type: 'document',
  fields: [
    defineField({
      name: 'authorType',
      type: 'reference',
      to: [{type: 'author'}],
    }),
    defineField({
      name: 'eventType',
      type: 'reference',
      to: [{type: 'event'}],
    }),
    defineField({
      name: 'date',
      type: 'datetime',
    }),
    defineField({
      name: 'header',
      type: 'string',
    }),
    defineField({
      name: 'image',
      type: 'image',
    }),
defineField({
      name: 'body',
      type: 'array',
      of: [{type: 'block'}],
    }),
    defineField({
      name: 'link',
      type: 'url',
    }),
  ],
})