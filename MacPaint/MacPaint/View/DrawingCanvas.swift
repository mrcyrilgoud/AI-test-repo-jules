import SwiftUI

struct DrawingCanvas: View {
    @ObservedObject var viewModel: DrawingViewModel

    var body: some View {
        GeometryReader { geometry in
            Canvas { context, size in
                if let image = viewModel.backgroundImage {
                    context.draw(Image(nsImage: image), in: CGRect(origin: .zero, size: size))
                }

                for line in viewModel.lines {
                    var path = Path()
                    path.addLines(line.points)
                    context.stroke(path, with: .color(line.color), lineWidth: line.lineWidth)
                }

                if let previewLine = viewModel.previewLine {
                    var path = Path()
                    path.addLines(previewLine.points)
                    context.stroke(path, with: .color(previewLine.color), lineWidth: previewLine.lineWidth)
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
            .onAppear {
                viewModel.canvasSize = geometry.size
            }
            .onChange(of: geometry.size) { newSize in
                viewModel.canvasSize = newSize
            }
        }
    }
}
