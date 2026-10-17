import AppKit

// Public, bundled macOS app artwork only. No installed-app inventory or user data.
let apps = [
    ("finder", "/System/Library/CoreServices/Finder.app"),
    ("safari", "/System/Cryptexes/App/System/Applications/Safari.app"),
    ("mail", "/System/Applications/Mail.app"),
    ("messages", "/System/Applications/Messages.app"),
    ("reminders", "/System/Applications/Reminders.app"),
    ("calendar", "/System/Applications/Calendar.app")
]
let destination = CommandLine.arguments[1]
for (name, path) in apps {
    guard FileManager.default.fileExists(atPath: path) else { fatalError("Missing \(path)") }
    let image = NSWorkspace.shared.icon(forFile: path)
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 256, pixelsHigh: 256,
        bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
        colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    image.draw(in: NSRect(x: 0, y: 0, width: 256, height: 256))
    NSGraphicsContext.restoreGraphicsState()
    try bitmap.representation(using: .png, properties: [:])!.write(to:
        URL(fileURLWithPath: destination).appendingPathComponent("\(name).png"))
}
