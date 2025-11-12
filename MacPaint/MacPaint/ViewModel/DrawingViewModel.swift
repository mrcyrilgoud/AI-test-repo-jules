import SwiftUI
import AppKit

class DrawingViewModel: ObservableObject {
    @Published var lines: [Line] = []
    @Published var selectedColor: Color = .black
    @Published var selectedTool: DrawingTool = .pencil
    @Published var selectedLineWidth: CGFloat = 1.0
    @Published var backgroundImage: NSImage?
    @Published var canvasSize: CGSize = .zero
    @Published var previewLine: Line?

    private var isNewLine = true
    private var lineStartPoint: CGPoint = .zero

    func addPoint(_ point: CGPoint) {
        if selectedTool == .paintbucket {
            return
        }

        if isNewLine {
            startNewLine(point: point)
            isNewLine = false
        }

        if selectedTool == .line {
            previewLine?.points = [lineStartPoint, point]
        } else {
            lines[lines.count - 1].points.append(point)
        }
    }

    func startNewLine(point: CGPoint) {
        var color = selectedColor
        var lineWidth = selectedLineWidth

        switch selectedTool {
        case .pencil:
            break
        case .paintbrush:
            lineWidth *= 5
        case .eraser:
            color = .white
            lineWidth *= 10
        case .line:
            lineStartPoint = point
        default:
            break
        }

        let newLine = Line(points: [point], color: color, lineWidth: lineWidth, tool: selectedTool)

        if selectedTool == .line {
            previewLine = newLine
        }

        lines.append(newLine)
    }

    func endLine() {
        if selectedTool == .line {
            if let previewLine = previewLine {
                lines[lines.count - 1].points = previewLine.points
            }
            previewLine = nil
        }

        if let lastLine = lines.last, lastLine.points.count < 2 && selectedTool != .line {
            lines.removeLast()
        }

        isNewLine = true
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

    func exportImage() {
        let imageView = ExportImageView(lines: lines, backgroundImage: backgroundImage, canvasSize: canvasSize)
        let image = imageView.renderAsImage()

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
    var tool: DrawingTool
}
