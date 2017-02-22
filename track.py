import applescript, json
from datetime import datetime

# applescript to call for current track details
script = applescript.AppleScript('''
	on checkCurrentTrack()
		tell application "Spotify"
			set currentTrackId to id of current track
			return currentTrackId
		end tell
	end checkCurrentTrack

	on checkPlayerPlaying()
		tell application "Spotify"
			if player state is playing then
				return true
			end if
		end tell
	end checkPlayerPlaying

	on checkIfOpen()
		if application "Spotify" is running then
			return true
		else
			return false
		end if
	end checkIfOpen

	on checkPosition()
		tell application "Spotify"
			set trackDuration to duration of current track
			set currentPosition to player position
			set percentCompleted to (currentPosition / trackDuration) * 1000

			return percentCompleted
		end tell
	end checkPosition

	on getListenedEvent()
		tell application "Spotify"
			set trackId to id of current track
			set trackTitle to name of current track
			set trackArtist to artist of current track
			set totalPlays to played count of current track
			set currentPopularity to popularity of current track
			set trackDuration to duration of current track


			set trackInfo to {TrackId, trackTitle, trackArtist, totalPlays, currentPopularity, trackDuration}
		end tell
	end getListenedEvent
	''')

# builds dictionary for a unique listening event
def createListenedEvent(today, spotify_id, title, artist, plays, popularity, length):
	return {'spotifyId': spotify_id,
			'title': title,
			'artist': artist,
			'spotify_plays': plays,
			'popularity': popularity,
			'length': length,
			'timestamp': today.isoformat()}

# checks that spotify is running; returns True
def currentlyRunning():
	if script.call('checkIfOpen'):
		return script.call('checkPlayerPlaying')

# while spotify is playing check for listened event
# at 90% of song, record unique event if player's 
# starting position is less than 90% of current track
def startListening():
	stopped_position = script.call('checkPosition')
	if stopped_position < .9:
		track_id = script.call('checkCurrentTrack')
		while (script.call('checkCurrentTrack') == track_id) and currentlyRunning():
			if script.call('checkPosition') > .9:
				return script.call('getListenedEvent')
				break
	else:
		return False	

def main():
	date = datetime.now()
	current_session = []
	while currentlyRunning():
		listened_to = startListening()
		if listened_to:
			listened_event = createListenedEvent(date, *listened_to)
			current_session.append(listened_event)
	if len(current_session) > 0:
		print(current_session)

if __name__ == "__main__":
    main()
