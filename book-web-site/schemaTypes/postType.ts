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
      name: 'draft',
      type: 'array',
      of: [{type: 'block'}],
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
      name: 'tweet_id',
      type: 'string',
      readOnly: true
    }),
    defineField({
      name: 'image',
      type: 'image',
    })
  ],
})