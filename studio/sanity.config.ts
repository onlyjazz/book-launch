import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {visionTool} from '@sanity/vision'
import {schemaTypes} from './schemaTypes'
import {markdownSchema} from 'sanity-plugin-markdown'
export default defineConfig({
  "name": 'default',
  "title": 'next-page-ai',

  "projectId": 'rh2kgtdt',
  "dataset": 'production',

  "plugins": [structureTool(), visionTool()],

  "schema": {
    "types": schemaTypes,
  },
})
