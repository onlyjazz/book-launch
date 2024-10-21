import {defineCliConfig} from 'sanity/cli'

export default defineCliConfig({
  studioHost: 'nextpage',
  api: {
    projectId: 'rh2kgtdt',
    dataset: 'production'
  },
  /**
   * Enable auto-updates for studios.
   * Learn more at https://www.sanity.io/docs/cli#auto-updates
   */
  autoUpdates: true,
})
