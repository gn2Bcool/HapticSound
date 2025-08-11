import Foundation
import ScreenCaptureKit
import AVFoundation

class AudioLevelMonitor: NSObject, SCStreamOutput {
    private var stream: SCStream?

    func startMonitoring() {
        SCShareableContent.getExcludingDesktopWindows(true, onScreenWindowsOnly: true) { content, error in
            guard let content = content, error == nil else {
                print("❌ Error fetching shareable content: \(error?.localizedDescription ?? "Unknown error")")
                return
            }

            guard let display = content.displays.first else {
                print("❌ No display found.")
                return
            }

            let filter = SCContentFilter(display: display, excludingWindows: [])

            let config = SCStreamConfiguration()
            config.capturesAudio = true
            config.sampleRate = 44100
            config.channelCount = 2
            config.showsCursor = false
            config.width = display.width
            config.height = display.height

            self.stream = SCStream(filter: filter, configuration: config, delegate: nil)

            do {
                try self.stream?.addStreamOutput(self, type: .audio, sampleHandlerQueue: DispatchQueue(label: "AudioSampleQueue"))
                try self.stream?.startCapture()
                print("🎙️ Audio capture started. Monitoring levels...")
            } catch {
                print("❌ Failed to start stream: \(error)")
            }
        }
    }

    func stream(_ stream: SCStream, didOutputSampleBuffer sampleBuffer: CMSampleBuffer, of type: SCStreamOutputType) {
    guard type == .audio else { return }

    guard let blockBuffer = CMSampleBufferGetDataBuffer(sampleBuffer) else { return }

    var lengthAtOffset = 0
    var totalLength = 0
    var dataPointer: UnsafeMutablePointer<Int8>?

    let status = CMBlockBufferGetDataPointer(
        blockBuffer,
        atOffset: 0,
        lengthAtOffsetOut: &lengthAtOffset,
        totalLengthOut: &totalLength,
        dataPointerOut: &dataPointer
    )

    if status == kCMBlockBufferNoErr, let pointer = dataPointer {
        let floatPointer = UnsafeRawPointer(pointer).assumingMemoryBound(to: Float32.self)
        let sampleCount = totalLength / MemoryLayout<Float32>.size

        let samples = UnsafeBufferPointer(start: floatPointer, count: sampleCount)

        let rms = sqrt(samples.map { $0 * $0 }.reduce(0, +) / Float(samples.count))
        let db = 20 * log10(rms)

        print(String(format: "%.2f", db))
        fflush(stdout)

        // ✅ Stop the run loop after first buffer
        //CFRunLoopStop(CFRunLoopGetMain())
    }
}
}

@main
struct Main {
    static func main() {
        setbuf(stdout, nil)
        let monitor = AudioLevelMonitor()
        monitor.startMonitoring()
        RunLoop.main.run()
    }
}
