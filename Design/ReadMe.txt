Stuff on the overall design and protocols will go here, probibly.

each file should have the ability to tag files, specifically to make organizing files during initial download just a little easier when picking which files to download
disk torrent mode
	in cases where there are too many files, the torrent can become essentially a read only virtual disk.
	You download a manifest, and the manifest tells you which blocks contain which files.
signed HTTP mirrors
	a file could have a http link to download it as auxillery, but the URL would need to be signed by the same person that made the torrent
	The signiture should help prevent unauthorised people from 'hijacking' the magnit URI, or worse, let someone make a lazy implimentation of the machinery for downloading which bypasses aditional security.
