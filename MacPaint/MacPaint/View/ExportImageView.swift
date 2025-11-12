import SwiftUI

struct ExportImageView: View {
    let lines: [Line]
    let backgroundImage: NSImage?
    let canvasSize: CGSize

    var body: some View {
        ZStack {
            if let backgroundImage = backgroundImage {
                Image(nsImage: backgroundImage)
                    .resizable()
                    .aspectRatio(contentMode: .fit)
            }
            Canvas { context, size in
                for line in lines {
                    var path = Path()
                    path.addLines(line.points)
                    context.stroke(path, with: .color(line.color), lineWidth: line.lineWidth)
                }
            }
        }
        .frame(width: canvasSize.width, height: canvasSize.height)
    }
}
