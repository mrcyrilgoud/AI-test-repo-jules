import SwiftUI
import AppKit

class DrawingViewModel: ObservableObject {
    @Published var lines: [Line] = []
    @Published var selectedColor: Color = .black
    @Published var selectedTool: DrawingTool = .pencil
    @Published var selectedLineWidth: CGFloat = 1.0
    @Published var backgroundImage: NSImage?

    func addPoint(_ point: CGPoint) {
        if lines.isEmpty || lines.last?.points.isEmpty == false {
            startNewLine()
        }
        lines[lines.count - 1].points.append(point)
    }

    func startNewLine() {
        let newLine = Line(points: [], color: selectedColor, lineWidth: selectedLineWidth)
        lines.append(newLine)
    }

    func endLine() {
        if lines.last?.points.count == 0 {
            lines.removeLast()
        }
    }

    func importImage() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [.png, .jpeg]
        if panel.runModal() == .OK {
            if let url = panel.url, let image = NSImage(contentsOf: url) {
                self.backgroundImage = image
            }
        }
    }

    func exportImage(view: some View) {
        let image = view.renderAsImage()

        let savePanel = NSSavePanel()
        savePanel.allowedContentTypes = [.png]
        if savePanel.runModal() == .OK {
            if let url = savePanel.url {
                let pngData = image?.tiffRepresentation(using: .png, factor: 1.0)
                try? pngData?.write(to: url)
            }
        }
    }
}

enum DrawingTool {
    case pencil
    case paintbrush
    case eraser
    case paintbucket
    case line
}

struct Line {
    var points: [CGPoint]
    var color: Color
    var lineWidth: CGFloat
}
