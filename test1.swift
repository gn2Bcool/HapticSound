audioRecorder.updateMeters()
let level = audioRecorder.averagePower(forChannel: 0)

print(level)