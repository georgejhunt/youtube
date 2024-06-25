describe('video player page', () => {
  beforeEach(() => {
    cy.intercept('GET', '/channel.json', { fixture: 'channel/channel.json' }).as('getChannel')
    cy.intercept('GET', '/playlists/uploads_from_openzim_testing-917Q.json', {
      fixture: 'channel/playlists/uploads_from_openzim_testing-917Q.json'
    }).as('getUploads')
    cy.visit('/')
    cy.wait('@getChannel')
    cy.wait('@getUploads')
  })

  it('loads the video and related information', () => {
    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel//videos/timelapse-9Tgo.json'
    }).as('getVideo')
    cy.contains('.v-card-title ', 'Timelapse').click()
    cy.wait('@getVideo')

    cy.url().should('include', '/watch')
    cy.contains('.video-title', 'Timelapse')
    cy.contains('.video-date', 'Published on Jun 4, 2024')
    cy.contains('.video-channel', 'openZIM_testing')
    cy.contains('.video-description', 'This is a short video of a timelapse.')
  })

  it('loads the playlist panel', () => {
    cy.intercept('GET', '/playlists.json', { fixture: 'channel/playlists.json' }).as('getPlaylists')
    cy.intercept('GET', '/playlists/timelapses-QgGI.json', {
      fixture: 'channel/playlists/timelapses-QgGI.json'
    }).as('getPlaylist')
    cy.intercept('GET', '/videos/timelapse-9Tgo.json', {
      fixture: 'channel/videos/timelapse-9Tgo.json'
    }).as('getVideo1')
    cy.intercept('GET', '/videos/cloudy_sky_time_lapse-k02q.json', {
      fixture: 'channel/videos/cloudy_sky_time_lapse-k02q.json'
    }).as('getVideo2')

    cy.contains('.v-btn__content', 'Playlists').click()
    cy.wait('@getPlaylists')

    cy.contains('.v-card-title ', 'Timelapses').click()
    cy.url().should('include', 'watch/timelapse-9Tgo?list=timelapses-QgGI')

    cy.wait('@getPlaylist')
    cy.wait('@getVideo1')

    cy.contains('Timelapses').should('be.visible')
    cy.contains('openZIM_testing - 1/2').should('be.visible')

    cy.contains('Cloudy Sky Time Lapse').click()
    cy.contains('openZIM_testing - 2/2').should('be.visible')
  })
})
