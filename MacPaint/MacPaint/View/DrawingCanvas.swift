import SwiftUI

struct DrawingCanvas: View {
    @ObservedObject var viewModel: DrawingViewModel

    var body: some View {
        Canvas { context, size in
            if let image = viewModel.backgroundImage {
                context.draw(Image(nsImage: image), in: CGRect(origin: .zero, size: size))
            }

            for line in viewModel.lines {
                var path = Path()
                path.addLines(line.points)
                context.stroke(path, with: .color(line.color), lineWidth: line.lineWidth)
            }
        }
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { value in
                    viewModel.addPoint(value.location)
                }
                .onEnded { _ in
                    viewModel.endLine()
                }
        )
    }
}
