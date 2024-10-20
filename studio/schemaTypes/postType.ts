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
      name: 'approved',
      type: 'boolean',
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
      name: 'prompt_identifier',
      type: 'string',
    }),
    defineField({
      name: 'impressions',
      type: 'number',
    }),
    defineField({
      name: 'engagement_rate',
      type: 'number',
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